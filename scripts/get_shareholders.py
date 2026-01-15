# -*- coding: utf-8 -*-
"""
获取十大股东信息

用法:
    python get_shareholders.py 002475
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


def get_shareholders(code: str, use_cache: bool = True):
    """获取主要股东"""
    print(f"获取股东信息: {code}")
    
    if use_cache:
        cached_data = cache_get('shareholders', code)
        if cached_data:
            print("从缓存加载数据...")
            display_holders(pd.DataFrame(cached_data))
            return

    try:
        df = ak.stock_main_stock_holder(stock=code)
        
        if df is not None and not df.empty:
            if use_cache:
                cache_set('shareholders', df.to_dict('records'), code)
                
            display_holders(df)
        else:
            print("未获取到数据")
            
    except Exception as e:
        print(f"获取失败: {e}")


def display_holders(df: pd.DataFrame):
    """显示股东信息"""
    if len(df) > 0:
        latest_date = df['截至日期'].max()
        latest = df[df['截至日期'] == latest_date]
        
        print(f"\n截至日期: {latest_date}")
        if '股东总数' in latest.columns:
            print(f"股东总数: {latest['股东总数'].iloc[0]}")
            print(f"平均持股: {latest['平均持股数'].iloc[0]}")
            
        print("\n十大股东:")
        cols = ['排名', '股东名称', '持股数量', '持股比例', '股本性质', '变动比例']
        # 映射列名
        col_map = {'编号': '排名'}
        latest = latest.rename(columns=col_map)
        
        show_cols = [c for c in cols if c in latest.columns]
        print(latest[show_cols].to_string(index=False))


def main():
    parser = argparse.ArgumentParser(description='获取股东信息')
    parser.add_argument('code', help='股票代码')
    parser.add_argument('--no-cache', action='store_true', help='不使用缓存')
    
    args = parser.parse_args()
    
    get_shareholders(args.code, use_cache=not args.no_cache)


if __name__ == '__main__':
    main()
