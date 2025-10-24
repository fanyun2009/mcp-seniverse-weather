from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
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
        ...

    def cache_weather(self,weather_data:Dict[str,Any]):
        """添加天气缓存"""
        ...

@asynccontextmanager
async def weather_lifespan(server:Server)->AsyncIterator[WeatherServerCotext]:
    """管理服务器生命周期"""
    ...