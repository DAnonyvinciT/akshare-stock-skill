# -*- coding: utf-8 -*-
"""
获取历史 K 线数据

用法:
    python get_history_kline.py 002475
    python get_history_kline.py 002475 --days 60
    python get_history_kline.py 002475 --start 20240101 --end 20241231
"""
import argparse
import sys
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

try:
    import akshare as ak
    import pandas as pd
except ImportError:
    print("请先安装依赖: pip install akshare pandas")
    sys.exit(1)

from cache_manager import cache_get, cache_set


def get_history_kline(code: str, period: str = 'daily', start_date: str = None, end_date: str = None, adjust: str = 'qfq', use_cache: bool = True):
    """
    获取历史行情数据
    
    Args:
        code: 股票代码
        period: 周期 (daily, weekly, monthly)
        start_date: 开始日期 YYYYMMDD
        end_date: 结束日期 YYYYMMDD
        adjust: 复权 (qfq=前复权, hfq=后复权, ""=不复权)
        use_cache: 是否使用缓存
    """
    # 默认最近365天
    if not end_date:
        end_date = datetime.now().strftime('%Y%m%d')
    if not start_date:
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
        
    print(f"获取数据: {code} ({start_date} - {end_date})")
    
    # 缓存键
    cache_key = f"{code}_{period}_{start_date}_{end_date}_{adjust}"
    
    # 尝试从缓存获取
    if use_cache:
        cached_data = cache_get('daily_kline', cache_key)
        if cached_data:
            print("从缓存加载数据...")
            return pd.DataFrame(cached_data)
    
    try:
        df = ak.stock_zh_a_hist(
            symbol=code,
            period=period,
            start_date=start_date,
            end_date=end_date,
            adjust=adjust
        )
        
        if df is None or df.empty:
            print("未获取到数据")
            return None
            
        print(f"获取成功: {len(df)} 条记录")
        
        # 写入缓存 (转换为 dict 列表)
        if use_cache:
            cache_set('daily_kline', df.to_dict('records'), cache_key)
            
        return df
        
    except Exception as e:
        print(f"获取失败: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='获取历史K线数据')
    parser.add_argument('code', help='股票代码')
    parser.add_argument('--days', type=int, default=60, help='最近N天')
    parser.add_argument('--start', help='开始日期 YYYYMMDD')
    parser.add_argument('--end', help='结束日期 YYYYMMDD')
    parser.add_argument('--period', default='daily', help='周期: daily/weekly/monthly')
    parser.add_argument('--adjust', default='qfq', help='复权: qfq/hfq/""')
    parser.add_argument('--no-cache', action='store_true', help='不使用缓存')
    
    args = parser.parse_args()
    
    start_date = args.start
    if not start_date and not args.end:
        start_date = (datetime.now() - timedelta(days=args.days)).strftime('%Y%m%d')
        
    df = get_history_kline(
        args.code, 
        args.period, 
        start_date, 
        args.end, 
        args.adjust,
        use_cache=not args.no_cache
    )
    
    if df is not None:
        print("\n数据预览 (最近10天):")
        print(df.tail(10).to_string(index=False))


if __name__ == '__main__':
    main()
