from typing import Dict, Any

import mcp
from mcp import Tool
from mcp.server import Server, InitializationOptions, NotificationOptions
from mcp.server.lowlevel.server import lifespan

from mcp_seniverse_weather_galaxy.weather_server_context import weather_lifespan

async def run_server():
    """启动并运行服务器"""
    server = WeatherServer()
    async with mcp.sever.stdio.stdio_server() as (read_stream,write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="weather",
                server_version="0.5.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            ),
        )

class WeatherServer(Server):
    """天气预报服务器,集成生命周期管理和工具调用"""
    def __init_(self):
        super.__init__(
            "Weather",
            lifespan=weather_lifespan
        )
        self._setup_handlers()

    def _setup_handlers(self):
        """注册请求处理器"""
        ...

    def _handler_list_tools(self) ->list[Tool]:
        """处理工具列表请求"""
        ...

    def _handle_call_tools(self)->Dict[str,Any]:
        """处理工具调用请求"""
        ...
