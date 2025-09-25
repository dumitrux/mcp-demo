# server.py
from mcp.server.fastmcp import FastMCP
import httpx

# Create an MCP server
mcp = FastMCP("weather-mcp-server")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# @mcp.tool()
# async def get_geo(city: str) -> str:
#     """Get geocoding data for a location.

#     Args:
#         city: City name
#     """

#     geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(geocoding_url, timeout=30.0)
#             result = response.json()
#             latitude = result["results"][0]["latitude"]
#             longitude = result["results"][0]["longitude"]
#             return f"Latitude: {latitude}, Longitude: {longitude}"
#         except Exception:
#             return "Unable to fetch geocoding data."

@mcp.tool()
async def get_forecast(city: str) -> str:
    """Get weather forecast for a location.

    Args:
        city: City name
    """

    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(geocoding_url, timeout=30.0)
            result = response.json()
            latitude = result["results"][0]["latitude"]
            longitude = result["results"][0]["longitude"]
        except Exception:
            result = "Unable to fetch geocoding data."

    forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,uv_index_max&hourly=temperature_2m&current=temperature_2m,precipitation,rain"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(forecast_url, timeout=30.0)
            forecast_data = response.json()
            return forecast_data
        except Exception:
            return "Unable to fetch weather data."

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# # Add a prompt
# @mcp.prompt()
# def greet_user(name: str, style: str = "friendly") -> str:
#     """Generate a greeting prompt"""
#     styles = {
#         "friendly": "Please write a warm, friendly greeting",
#         "formal": "Please write a formal, professional greeting",
#         "casual": "Please write a casual, relaxed greeting",
#     }

#     return f"{styles.get(style, styles['friendly'])} for someone named {name}."

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')