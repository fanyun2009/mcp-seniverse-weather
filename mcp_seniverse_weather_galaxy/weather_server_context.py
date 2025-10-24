import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Dict, Any

from mcp.server import Server

from mcp_seniverse_weather_galaxy.cache_entry import CacheEntry


class WeatherServerCotext:
    """天气服务上下文，管理服务器缓存和状态"""
    def __init__(self,api_key:str):
        # 服务器状态"
        self.api_key = api_key
        self.api_calls = 0
        self.api_hits = 0
        self.api_misses = 0

        # 缓存存储
        self.weather_cache:Dict[str,CacheEntry] = {}

    def get_cache_weather(self,city:str)->Dict[str,Any] | None:
        """获取天气缓存"""
        if city not in self.weather_cache:
            self.api_misses+=1
            return None
        entry = self.weather_cache[city]
        if entry.expirre_at < datetime.now():
            self.api_misses+=1
            del self.weather_cache[city]
            return None
        return entry.data

    def cache_weather(self,city:str,weather_data:Dict[str,Any]):
        """添加天气缓存,设置5分钟的过期时间"""
        expire_at = datetime.now() + timedelta(minutes=5)
        self.weather_cache[city] = CacheEntry(weather_data,expire_at)


@asynccontextmanager
async def weather_lifespan(server:Server)->AsyncIterator[WeatherServerCotext]:
    """管理服务器生命周期"""
    api_key = os.getenv("SENIVERSE_API_KEY")
    if not api_key:
        raise ValueError("SENIVERSE_API_KEY环境变量未设置")
    ctx = WeatherServerCotext(api_key)

    try:
        yield ctx
    finally:
        # 服务器输出统计信息
        total_queries = ctx.api_hits+ctx.api_misses
        hit_rate =(ctx.api_hits/total_queries*100) if total_queries>0 else 0
        print(f"服务器运算统计")
        print(f"-API调用次数：{total_queries}")
        print(f"-缓存命中次数：{ctx.api_hits}")
        print(f"-缓存未命中次数：{ctx.api_misses}")
        print(f"-缓存命中率：{hit_rate}%")
