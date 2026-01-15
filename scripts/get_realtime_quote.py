# -*- coding: utf-8 -*-
"""
获取股票实时行情

用法:
    python get_realtime_quote.py 002475
    python get_realtime_quote.py 002475 600519
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


def get_realtime_quote(codes: list, Use_markdown: bool = True, use_cache: bool = True):
    """获取实时行情"""
    print("正在获取实时行情...")
    
    # 尝试从缓存获取 (全量市场数据)
    df = None
    if use_cache:
        cached_data = cache_get('realtime', 'market_spot')
        if cached_data:
            # print("从缓存加载市场数据...")
            df = pd.DataFrame(cached_data)
    
    if df is None:
        try:
            df = ak.stock_zh_a_spot_em()
            # 写入缓存
            if use_cache:
                cache_set('realtime', df.to_dict('records'), 'market_spot')
        except Exception as e:
            print(f"获取失败: {e}")
            return
    
    if df is not None:
        result = df[df['代码'].isin(codes)]
        if len(result) > 0:
            if Use_markdown:
                print(result.to_markdown(index=False))
            else:
                print(result.to_string(index=False))
        else:
            print(f"未找到代码: {codes}")


def main():
    parser = argparse.ArgumentParser(description='获取实时行情')
    parser.add_argument('codes', nargs='+', help='股票代码列表')
    parser.add_argument('--no-cache', action='store_true', help='不使用缓存')
    
    args = parser.parse_args()
    
    get_realtime_quote(args.codes, use_cache=not args.no_cache)


if __name__ == '__main__':
    main()
