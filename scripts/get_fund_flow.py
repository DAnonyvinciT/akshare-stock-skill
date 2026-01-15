# -*- coding: utf-8 -*-
"""
获取资金流向数据

用法:
    python get_fund_flow.py 002475
    python get_fund_flow.py 002475 --days 30
"""
import argparse
import sys
import warnings
warnings.filterwarnings('ignore')

try:
    import akshare as ak
    import pandas as pd
except ImportError:
    print("请先安装依赖: pip install akshare pandas")
    sys.exit(1)

from cache_manager import cache_get, cache_set


def get_market(code: str) -> str:
    return 'sh' if code.startswith('6') else 'sz'


def get_fund_flow(code: str, days: int = 10, use_cache: bool = True):
    """获取个股资金流向"""
    market = get_market(code)
    print(f"获取资金流向: {code} ({market})")
    
    # 缓存 Key: code_days (注意: 流向数据更新频繁，缓存时间应较短)
    cache_key = f"{code}_{market}"
    
    df = None
    if use_cache:
        cached_data = cache_get('fund_flow', cache_key)
        if cached_data:
            print("从缓存加载数据...")
            df = pd.DataFrame(cached_data)
    
    if df is None:
        try:
            df = ak.stock_individual_fund_flow(stock=code, market=market)
            if df is not None and not df.empty:
                # 写入缓存
                if use_cache:
                    cache_set('fund_flow', df.to_dict('records'), cache_key, expire_seconds=3600)
        except Exception as e:
            print(f"获取失败: {e}")
            return

    if df is not None:
        print(f"\n最近 {days} 天资金流向:")
        recent = df.tail(days)
        
        # 简化显示列
        cols = ['日期', '收盘价', '涨跌幅', '主力净流入-净额', '主力净流入-净占比', '超大单净流入-净额']
        # 检查列是否存在
        show_cols = [c for c in cols if c in recent.columns]
        
        # 格式化金额 (元 -> 万/亿)
        format_df = recent[show_cols].copy()
        for col in ['主力净流入-净额', '超大单净流入-净额']:
            if col in format_df.columns:
                format_df[col] = format_df[col].apply(lambda x: f"{x/10000:.0f}万" if abs(x) < 1e8 else f"{x/1e8:.2f}亿")
                
        print(format_df.to_string(index=False))
        
        # 统计
        total_in = recent['主力净流入-净额'].sum()
        print("-" * 50)
        print(f"{days}日主力净流入合计: {total_in/1e8:.2f} 亿元")


def main():
    parser = argparse.ArgumentParser(description='获取资金流向')
    parser.add_argument('code', help='股票代码')
    parser.add_argument('--days', type=int, default=10, help='显示最近N天')
    parser.add_argument('--no-cache', action='store_true', help='不使用缓存')
    
    args = parser.parse_args()
    
    get_fund_flow(args.code, args.days, use_cache=not args.no_cache)


if __name__ == '__main__':
    main()
