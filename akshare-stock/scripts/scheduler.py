# -*- coding: utf-8 -*-
"""
定时任务调度器

功能:
- 每日收盘后自动获取数据
- 定时生成分析报告
- 可配置监控股票列表

用法:
    python scheduler.py              # 运行调度器
    python scheduler.py --run-now    # 立即执行一次
    python scheduler.py --report     # 生成报告
"""
import argparse
import os
import sys
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

try:
    import yaml
except ImportError:
    print("请安装 pyyaml: pip install pyyaml")
    yaml = None

# 脚本目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SKILL_DIR, 'config.yaml')


def load_config() -> dict:
    """加载配置文件"""
    if not os.path.exists(CONFIG_PATH):
        return get_default_config()
    
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"配置文件加载失败: {e}")
        return get_default_config()


def get_default_config() -> dict:
    """默认配置"""
    return {
        'watchlist': [
            {'code': '002475', 'name': '立讯精密'},
        ],
        'scheduler': {
            'enabled': True,
            'daily_fetch_time': '15:30',
        },
        'output': {
            'report_dir': './reports',
            'format': 'markdown',
        }
    }


def fetch_stock_data(code: str):
    """获取单只股票数据"""
    from get_realtime_quote import get_realtime_quote
    from get_history_kline import get_history_kline
    from get_valuation import get_valuation
    from get_fund_flow import get_fund_flow
    
    print(f"正在获取 {code} 数据...")
    
    try:
        get_realtime_quote([code], use_cache=False)
        print(f"  ✓ 实时行情")
    except Exception as e:
        print(f"  ✗ 实时行情: {e}")
    
    try:
        get_history_kline(code, use_cache=False)
        print(f"  ✓ 历史K线")
    except Exception as e:
        print(f"  ✗ 历史K线: {e}")
    
    try:
        get_valuation(code, use_cache=False)
        print(f"  ✓ 估值指标")
    except Exception as e:
        print(f"  ✗ 估值指标: {e}")
    
    try:
        get_fund_flow(code, use_cache=False)
        print(f"  ✓ 资金流向")
    except Exception as e:
        print(f"  ✗ 资金流向: {e}")


def generate_report(config: dict):
    """生成分析报告"""
    from analyze_investment import InvestmentAnalyzer
    
    report_dir = config.get('output', {}).get('report_dir', './reports')
    
    # 确保报告目录存在
    os.makedirs(report_dir, exist_ok=True)
    
    watchlist = config.get('watchlist', [])
    
    all_reports = ["# 股票分析报告汇总\n"]
    all_reports.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    all_reports.append("---\n")
    
    for stock in watchlist:
        code = stock['code']
        name = stock.get('name', code)
        print(f"正在分析 {name} ({code})...")
        
        try:
            analyzer = InvestmentAnalyzer(code)
            report = analyzer.generate_report()
            
            # 保存单只股票报告
            filename = f"{code}_{datetime.now().strftime('%Y%m%d')}.md"
            filepath = os.path.join(report_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"  ✓ 已保存: {filepath}")
            
            all_reports.append(report)
            all_reports.append("\n---\n")
        except Exception as e:
            print(f"  ✗ 分析失败: {e}")
    
    # 保存汇总报告
    summary_file = os.path.join(report_dir, f"summary_{datetime.now().strftime('%Y%m%d')}.md")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_reports))
    print(f"\n汇总报告已保存: {summary_file}")


def run_daily_task(config: dict):
    """执行每日任务"""
    print(f"\n{'='*50}")
    print(f"执行每日任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")
    
    watchlist = config.get('watchlist', [])
    
    # 获取数据
    for stock in watchlist:
        fetch_stock_data(stock['code'])
        time.sleep(1)  # 避免请求过快
    
    # 生成报告
    generate_report(config)
    
    print(f"\n每日任务完成!")


def run_scheduler(config: dict):
    """运行调度器"""
    if not config.get('scheduler', {}).get('enabled', False):
        print("定时任务未启用，请在 config.yaml 中设置 scheduler.enabled: true")
        return
    
    daily_time = config.get('scheduler', {}).get('daily_fetch_time', '15:30')
    
    print(f"定时任务调度器已启动")
    print(f"每日执行时间: {daily_time}")
    print(f"监控股票: {len(config.get('watchlist', []))} 只")
    print(f"按 Ctrl+C 停止\n")
    
    while True:
        now = datetime.now()
        target_time = now.replace(
            hour=int(daily_time.split(':')[0]),
            minute=int(daily_time.split(':')[1]),
            second=0,
            microsecond=0
        )
        
        # 如果今天的时间已过，等到明天
        if now > target_time:
            target_time += timedelta(days=1)
        
        wait_seconds = (target_time - now).total_seconds()
        
        print(f"下次执行时间: {target_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"等待 {wait_seconds/3600:.1f} 小时...")
        
        try:
            time.sleep(wait_seconds)
            run_daily_task(config)
        except KeyboardInterrupt:
            print("\n调度器已停止")
            break


def main():
    parser = argparse.ArgumentParser(description='定时任务调度器')
    parser.add_argument('--run-now', action='store_true', help='立即执行一次')
    parser.add_argument('--report', action='store_true', help='仅生成报告')
    parser.add_argument('--fetch', action='store_true', help='仅获取数据')
    
    args = parser.parse_args()
    
    # 切换到脚本目录
    os.chdir(SCRIPT_DIR)
    
    if yaml is None:
        print("警告: 未安装 pyyaml，使用默认配置")
    
    config = load_config()
    
    if args.run_now:
        run_daily_task(config)
    elif args.report:
        generate_report(config)
    elif args.fetch:
        for stock in config.get('watchlist', []):
            fetch_stock_data(stock['code'])
    else:
        run_scheduler(config)


if __name__ == '__main__':
    main()
