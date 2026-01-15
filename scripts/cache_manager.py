# -*- coding: utf-8 -*-
"""
数据缓存管理器

功能:
- SQLite 本地缓存
- 自动过期管理
- 支持多种数据类型

用法:
    from cache_manager import CacheManager
    cache = CacheManager()
    cache.set('key', data, expire_seconds=3600)
    data = cache.get('key')
"""
import sqlite3
import json
import os
import hashlib
from datetime import datetime, timedelta
from typing import Any, Optional

# 默认缓存目录
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.cache')
DB_PATH = os.path.join(CACHE_DIR, 'akshare_cache.db')

# 缓存过期时间配置（秒）
CACHE_EXPIRE = {
    'realtime': 60,           # 实时行情: 1分钟
    'daily_kline': 3600,      # 日K线: 1小时
    'financial': 86400 * 7,   # 财务数据: 7天
    'shareholders': 86400 * 30,  # 股东数据: 30天
    'dividend': 86400 * 30,   # 分红数据: 30天
    'valuation': 3600,        # 估值数据: 1小时
    'fund_flow': 3600,        # 资金流向: 1小时
    'board': 86400,           # 板块数据: 1天
}


class CacheManager:
    """数据缓存管理器"""
    
    def __init__(self, db_path: str = None):
        """
        初始化缓存管理器
        
        Args:
            db_path: 数据库文件路径，默认使用 .cache/akshare_cache.db
        """
        self.db_path = db_path or DB_PATH
        self._ensure_cache_dir()
        self._init_db()
    
    def _ensure_cache_dir(self):
        """确保缓存目录存在"""
        cache_dir = os.path.dirname(self.db_path)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def _init_db(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    expire_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def _generate_key(self, category: str, *args, **kwargs) -> str:
        """
        生成缓存键
        
        Args:
            category: 数据类别（如 realtime, daily_kline）
            *args: 其他参数
            **kwargs: 关键字参数
        
        Returns:
            缓存键字符串
        """
        key_parts = [category] + list(args)
        if kwargs:
            key_parts.append(json.dumps(kwargs, sort_keys=True))
        raw_key = ':'.join(str(p) for p in key_parts)
        return hashlib.md5(raw_key.encode()).hexdigest()
    
    def set(self, key: str, value: Any, expire_seconds: int = 3600) -> bool:
        """
        设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值（会被 JSON 序列化）
            expire_seconds: 过期时间（秒）
        
        Returns:
            是否成功
        """
        try:
            expire_at = datetime.now() + timedelta(seconds=expire_seconds)
            value_json = json.dumps(value, default=str, ensure_ascii=False)
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO cache (key, value, expire_at)
                    VALUES (?, ?, ?)
                ''', (key, value_json, expire_at))
                conn.commit()
            return True
        except Exception as e:
            print(f"缓存写入失败: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存
        
        Args:
            key: 缓存键
        
        Returns:
            缓存值，如果不存在或已过期返回 None
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT value, expire_at FROM cache WHERE key = ?
                ''', (key,))
                row = cursor.fetchone()
                
                if row is None:
                    return None
                
                value_json, expire_at = row
                expire_time = datetime.fromisoformat(expire_at)
                
                if datetime.now() > expire_time:
                    # 已过期，删除并返回 None
                    self.delete(key)
                    return None
                
                return json.loads(value_json)
        except Exception as e:
            print(f"缓存读取失败: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('DELETE FROM cache WHERE key = ?', (key,))
                conn.commit()
            return True
        except Exception:
            return False
    
    def clear_expired(self) -> int:
        """清理所有过期缓存，返回清理数量"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    DELETE FROM cache WHERE expire_at < ?
                ''', (datetime.now(),))
                conn.commit()
                return cursor.rowcount
        except Exception:
            return 0
    
    def clear_all(self) -> bool:
        """清空所有缓存"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('DELETE FROM cache')
                conn.commit()
            return True
        except Exception:
            return False
    
    def get_stats(self) -> dict:
        """获取缓存统计信息"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # 总数
                total = conn.execute('SELECT COUNT(*) FROM cache').fetchone()[0]
                # 已过期数
                expired = conn.execute('''
                    SELECT COUNT(*) FROM cache WHERE expire_at < ?
                ''', (datetime.now(),)).fetchone()[0]
                # 数据库大小
                db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
                
                return {
                    'total': total,
                    'expired': expired,
                    'valid': total - expired,
                    'db_size_mb': round(db_size / 1024 / 1024, 2)
                }
        except Exception:
            return {}


# 全局缓存实例
_cache = None

def get_cache() -> CacheManager:
    """获取全局缓存实例"""
    global _cache
    if _cache is None:
        _cache = CacheManager()
    return _cache


def cache_get(category: str, *args, **kwargs):
    """快捷获取缓存"""
    cache = get_cache()
    key = cache._generate_key(category, *args, **kwargs)
    return cache.get(key)


def cache_set(category: str, value: Any, *args, expire_seconds: int = None, **kwargs):
    """快捷设置缓存"""
    cache = get_cache()
    key = cache._generate_key(category, *args, **kwargs)
    if expire_seconds is None:
        expire_seconds = CACHE_EXPIRE.get(category, 3600)
    return cache.set(key, value, expire_seconds)


if __name__ == '__main__':
    # 测试缓存
    cache = CacheManager()
    
    print("缓存管理器测试")
    print("-" * 40)
    
    # 设置缓存
    cache.set('test_key', {'name': '测试数据', 'value': 123}, expire_seconds=60)
    print("设置缓存: test_key")
    
    # 读取缓存
    data = cache.get('test_key')
    print(f"读取缓存: {data}")
    
    # 统计信息
    stats = cache.get_stats()
    print(f"缓存统计: {stats}")
    
    # 清理过期
    cleared = cache.clear_expired()
    print(f"清理过期缓存: {cleared} 条")
