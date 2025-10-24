from typing import Dict, Any

import mcp
import requests
from click import Parameter
from mcp.server import Server, InitializationOptions, NotificationOptions
from mcp.server.fastmcp.tools import Tool

from mcp_seniverse_weather_galaxy.weather_server_context import weather_lifespan, WeatherServerCotext


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
        super().__init__(
            "Weather",
            lifespan=weather_lifespan
        )
        self._setup_handlers()

    def _setup_handlers(self):
        """注册请求处理器"""
        # self.register_list_toos_handler(self._handler_list_tools())

    def _handler_list_tools(self) ->list[Tool]:
        """处理工具列表请求"""
        tool_list = []
        query_tool_desc = Tool(
            name="current_weather",
            description="根据输入城市，查询当前天气",
            parameters = [
                Parameter(
                    name="city",
                    description="city name",
                    type="string",
                    required=True
                )
            ]
        )
        tool_list.append(query_tool_desc)
        return tool_list

    def _handle_call_tools(self,name:str,arguments:Dict[str,Any])->Dict[str,Any]:
        """处理工具调用请求"""
        if name!="current_weather":
            raise ValueError(f"未知的工具{name}")
        city = arguments.get(name)
        if not city:
            raise ValueError(f"缺少城市")
        ctx:WeatherServerCotext = self.request_handlers.lifespan_context

        try:
            weather_data = ctx.get_cache_weather(name)
            if not weather_data:
                ctx.api_hits += 1
                weather_response = requests.get(
                    url="https://api.seniverse.com/v3/weather/now.json",
                    params={
                        "key": ctx.api_key,
                        "location": city,
                        "language": "zh-Hans",
                        "unit": "c"
                    }
                )
                weather_response.raise_for_status()
                data = weather_response.json()
                results = data.get("result", [])
                if not results:
                    return {"error", f"未找到城市 {city}的天气"}
                weather_data = results[0]
            return weather_data
        except requests.exceptions.RequestException as e:
            error_message = f"Weather API error:{e}"
            # 4xx/5xx的错误类型包含response
            try:
                if hasattr(e, 'response') and e.response is not None:
                    error_data = e.response.json()
                    if 'message' in error_data:
                        error_message = f"Weather API error: {error_data['message']}"
            except ValueError:
                pass
            return {"error": error_message}
