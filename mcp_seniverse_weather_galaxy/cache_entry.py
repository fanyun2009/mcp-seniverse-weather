import datetime
from typing import AnyStr, Dict


class CacheEntry:
    """缓存条目，包含缓存数据和过期时间"""
    def __init_(self,data:Dict[str,AnyStr],expire_at:datetime):
        self.data = data
        self.expirre_at = expire_at