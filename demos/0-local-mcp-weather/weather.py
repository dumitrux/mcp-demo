#!/usr/bin/env python3
"""
Model Context Protocol (MCP) Python server example that provides weather forecast.
"""

import httpx
import json
import logging

# Import FastMCP - the high-level MCP server API
from mcp.server.fastmcp import FastMCP

# Configure module logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an MCP server
mcp = FastMCP("weather-mcp-server")

# Add an addition tool
@mcp.tool()
def add_test(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Add a weather forecast tool
@mcp.tool()
async def get_forecast(city: str) -> str:
    """Get weather forecast for a location.

    Args:
        city: City name
    """

    logging.info(f"Fetching weather for city: {city}")

    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(geocoding_url, timeout=30.0)
            result = response.json()
            latitude = result["results"][0]["latitude"]
            longitude = result["results"][0]["longitude"]
        except Exception:
            result = "Unable to fetch geocoding data."

    forecast_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&daily=temperature_2m_max,temperature_2m_min,uv_index_max"
        f"&hourly=temperature_2m"
        f"&current_weather=true"
        f"&timezone=auto"
    )
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(forecast_url, timeout=30.0)
            response.raise_for_status()
            forecast_data = response.json()
            # Return a JSON string (tool expects a string). Keep UTF-8 and indentation for readability.
            return json.dumps(forecast_data, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"Unable to fetch weather data: {e}"

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

# Prompt for running a clothing recommendation model
@mcp.prompt()
def run_cloths_recommendation(day: str, city: str) -> str:
    """Generate a clothing recommendation prompt based on the weather forecast for the day."""
    return (
        f"Keep the answer short and concise."
        f"Based on the weather forecast for {day} in {city},"
        f"recommend appropriate clothing items from my closet"
    )

# Resource to list my cloths
@mcp.resource("my-closet://")
def get_cloths() -> str:
    """Get a list of all cloths in the closet"""
    logger.info("Retrieving all items from the closet.")

    closet_items = [
        # T-Shirts & Tops
        {"name": "Berlin Marathon 2023 Finisher T-Shirt", "description": "Berlin Marathon 2023 Finisher T-Shirt: Reflective technical shirt for running."},
        {"name": "Real Madrid 2024 Home Jersey", "description": "Real Madrid 2024 Home Jersey: Official team jersey for match days."},
        {"name": "Hawaiian Print Beach Shirt", "description": "Hawaiian Print Beach Shirt: Lightweight rayon, perfect for vacations."},
        {"name": "Basic Black Cotton T-Shirt", "description": "Basic Black Cotton T-Shirt: Versatile crew neck for everyday wear."},
        {"name": "Smart Navy Blue Polo Shirt", "description": "Smart Navy Blue Polo Shirt: Classic pique fabric for a smart-casual look."},
        {"name": "Thermal Base-Layer (Gray)", "description": "Thermal Base-Layer (Gray): Waffle-knit long-sleeve for cold weather."},
        {"name": "Band Logo Graphic Tee", "description": "Band Logo Graphic Tee: Vintage rock band concert t-shirt."},
        {"name": "Workout Tank Top (Lime)", "description": "Workout Tank Top (Lime): Moisture-wicking fabric for the gym."},

        # Pants & Shorts
        {"name": "Levi's 501 Dark Wash Jeans", "description": "Levi's 501 Dark Wash Jeans: Straight fit, classic five-pocket style."},
        {"name": "Slim-Fit Beige Chinos", "description": "Slim-Fit Beige Chinos: A smart alternative to jeans."},
        {"name": "Nike Fleece Joggers (Gray)", "description": "Nike Fleece Joggers (Gray): Comfortable sweatpants for lounging or workouts."},
        {"name": "Formal Wool Trousers (Charcoal)", "description": "Formal Wool Trousers (Charcoal): Tailored pants for business or events."},
        {"name": "Khaki Cargo Hiking Shorts", "description": "Khaki Cargo Hiking Shorts: Durable cotton with plenty of pockets for trails."},
        {"name": "Running Shorts (Blue, Lined)", "description": "Running Shorts (Blue, Lined): Lightweight athletic shorts with a built-in liner."},
        {"name": "Thermal Leggings (Black)", "description": "Thermal Leggings (Black): Base layer pants for skiing or winter sports."},

        # Outerwear
        {"name": "Packable Windbreaker (Black)", "description": "Packable Windbreaker (Black): Water-resistant shell jacket for travel."},
        {"name": "Classic Denim Trucker Jacket", "description": "Classic Denim Trucker Jacket: A timeless layering piece."},
        {"name": "Hooded Raincoat (Yellow)", "description": "Hooded Raincoat (Yellow): Fully waterproof jacket for heavy rain."},
        {"name": "Winter Parka (Olive Green)", "description": "Winter Parka (Olive Green): Down-filled coat with a faux-fur hood for deep cold."},
        {"name": "Leather Biker Jacket", "description": "Leather Biker Jacket: Asymmetric zip, classic rebellion style."},

        # Hats & Gloves
        {"name": "Wool Beanie (Charcoal)", "description": "Wool Beanie (Charcoal): Warm knit hat for cold winter days."},
        {"name": "NY Yankees Baseball Cap", "description": "NY Yankees Baseball Cap: Official team cap for sunny days."},
        {"name": "Leather Driving Gloves (Brown)", "description": "Leather Driving Gloves (Brown): Supple leather for grip and style."},
        {"name": "Waterproof Ski Gloves", "description": "Waterproof Ski Gloves: Insulated and durable for snow sports."},

        # Shoes
        {"name": "White Leather Sneakers", "description": "White Leather Sneakers: Classic low-top design, goes with everything."},
        {"name": "Black Oxford Dress Shoes", "description": "Black Oxford Dress Shoes: Polished leather for formal events and business meetings."},
        {"name": "Brown Leather Hiking Boots", "description": "Brown Leather Hiking Boots: Waterproof with ankle support for trails."},
        {"name": "Running Shoes (Black/White)", "description": "Running Shoes (Black/White): Cushioned and breathable for road running."},
        {"name": "Leather Flip-Flops", "description": "Leather Flip-Flops: Comfortable and durable sandals for the beach or casual summer wear."},
        {"name": "Chelsea Boots (Suede)", "description": "Chelsea Boots (Suede): Stylish and versatile pull-on boots for smart-casual outfits."}
    ]
    
    # The data is already in the correct format in the imported list.
    # We just need to wrap it in a dictionary and dump it to a JSON string.
    
    return json.dumps({"cloths": closet_items})


if __name__ == "__main__":
    logger.info(f"MCP Server initialized")
    
    # Run the server with stdio transport
    # This can be tested with one of these methods:
    # 1. Direct execution: python server.py
    # 2. MCP inspector: mcp dev server.py
    # 3. Install in Claude Desktop: mcp install server.py
    mcp.run()
