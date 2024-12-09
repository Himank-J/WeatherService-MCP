import json
import logging
import aiohttp
from typing import Any
from pydantic import AnyUrl
from mcp.server import Server
from collections.abc import Sequence
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
from data_request import fetch_weather, fetch_forecaset
from config import API_KEY, API_BASE_URL, CURRENT_WEATHER_ENDPOINT, DEFAULT_CITY, FORECAST_ENDPOINT, http_params

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server-weather-app")

app = Server("weather-server")

@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available weather resources."""
    uri = AnyUrl(f"weather://{DEFAULT_CITY}/current")
    return [
        Resource(
            uri=uri,
            name=f"Current weather in {DEFAULT_CITY}",
            mimeType="application/json",
            description="Real-time weather data"
        )
    ]

@app.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    """Read current weather data for a city."""
    city = DEFAULT_CITY
    if str(uri).startswith("weather://") and str(uri).endswith("/current"):
        city = str(uri).split("/")[-2]
    else:
        raise ValueError(f"Unknown resource: {uri}")

    try:
        weather_data = await fetch_weather(city)
        return json.dumps(weather_data, indent=2)
    
    except Exception as e:
        raise RuntimeError(f"Weather API error: {str(e)}")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available weather tools."""
    return [
        Tool(
            name="get_forecast",
            description="Get weather forecast for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    },
                    "days": {
                        "type": "number",
                        "description": "Number of days (1-5)",
                        "minimum": 1,
                        "maximum": 5
                    }
                },
                "required": ["city"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls for weather forecasts."""
    
    if name != "get_forecast":
        raise ValueError(f"Unknown tool: {name}")

    if not isinstance(arguments, dict) or "city" not in arguments:
        raise ValueError("Invalid forecast arguments")

    city = arguments["city"]
    days = min(int(arguments.get("days", 3)), 5)

    try:
        forecast_data = fetch_forecaset(city, days)
        return [
            TextContent(
                type="text",
                text=json.dumps(forecast_data, indent=2)
            )
        ]
    except Exception as e:
        logger.error(f"Weather API error: {str(e)}")
        raise RuntimeError(f"Weather API error: {str(e)}")

async def main():
    from mcp.server.stdio import stdio_server

    logger.info('Starting server...')
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())