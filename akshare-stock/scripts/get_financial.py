# -*- coding: utf-8 -*-
"""
获取财务数据 (财务摘要)

用法:
    python get_financial.py 002475
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


def get_financial(code: str, use_cache: bool = True):
    """获取财务摘要 (同花顺)"""
    print(f"获取财务数据: {code}")
    
    if use_cache:
        cached_data = cache_get('financial', code)
        if cached_data:
            print("从缓存加载数据...")
            display_financial(pd.DataFrame(cached_data))
            return

    try:
        df = ak.stock_financial_abstract_ths(symbol=code, indicator="按报告期")
        
        if df is not None and not df.empty:
            display_financial(df)
            
            if use_cache:
                cache_set('financial', df.to_dict('records'), code)
        else:
            print("未获取到数据")
            
    except Exception as e:
        print(f"获取失败: {e}")


def display_financial(df: pd.DataFrame):
    """显示最新的财务数据"""
    if len(df) > 0:
        latest = df.iloc[0]
        print("-" * 40)
        print(f"报告期: {latest.get('报告期', '')}")
        print("-" * 40)
        print(f"净利润:       {latest.get('净利润', '')}")
        print(f"净利润同比:   {latest.get('净利润同比增长率', '')}")
        print(f"扣非净利润:   {latest.get('扣非净利润', '')}")
        print(f"营业总收入:   {latest.get('营业总收入', '')}")
        print(f"营收同比:     {latest.get('营业总收入同比增长率', '')}")
        print("-" * 40)
        print(f"基本每股收益: {latest.get('基本每股收益', '')}")
        print(f"每股净资产:   {latest.get('每股净资产', '')}")
        print(f"每股经营现金: {latest.get('每股经营现金流', '')}")
        print("-" * 40)
        print(f"净资产收益率: {latest.get('净资产收益率', '')}")
        print(f"销售毛利率:   {latest.get('销售毛利率', '')}")
        print(f"销售净利率:   {latest.get('销售净利率', '')}")
        print(f"资产负债率:   {latest.get('资产负债率', '')}")


def main():
    parser = argparse.ArgumentParser(description='获取财务数据')
    parser.add_argument('code', help='股票代码')
    parser.add_argument('--no-cache', action='store_true', help='不使用缓存')
    
    args = parser.parse_args()
    
    get_financial(args.code, use_cache=not args.no_cache)


if __name__ == '__main__':
    main()
