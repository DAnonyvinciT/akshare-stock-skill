# -*- coding: utf-8 -*-
"""
获取历史分红信息

用法:
    python get_dividend.py 002475
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


def get_dividend(code: str, use_cache: bool = True):
    """获取分红信息"""
    print(f"获取分红记录: {code}")
    
    if use_cache:
        cached_data = cache_get('dividend', code)
        if cached_data:
            print("从缓存加载数据...")
            print(pd.DataFrame(cached_data).head(10).to_string(index=False))
            return

    try:
        df = ak.stock_history_dividend_detail(symbol=code, indicator="分红")
        
        if df is not None and not df.empty:
            if use_cache:
                cache_set('dividend', df.to_dict('records'), code)
                
            print(df.head(10).to_string(index=False))
        else:
            print("未获取到分红数据")
            
    except Exception as e:
        print(f"获取失败: {e}")


def main():
    parser = argparse.ArgumentParser(description='获取分红信息')
    parser.add_argument('code', help='股票代码')
    parser.add_argument('--no-cache', action='store_true', help='不使用缓存')
    
    args = parser.parse_args()
    
    get_dividend(args.code, use_cache=not args.no_cache)


if __name__ == '__main__':
    main()
