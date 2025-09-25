#!/usr/bin/env python3
"""
Example MCP client for testing the Weather MCP server via Azure APIM.
"""

import asyncio
import httpx
import json
import os
import sys

class MCPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = httpx.AsyncClient()
        self.session_id = None
        
    async def initialize(self):
        """Initialize MCP session"""
        response = await self.session.post(
            self.base_url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            json={
                "jsonrpc": "2.0",  
                "id": "1",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "apim-weather-client",
                        "version": "1.0.0"
                    }
                }
            }
        )
        result = response.json()
        print("✅ MCP Session initialized")
        print(json.dumps(result, indent=2))
        return result
        
    async def list_tools(self):
        """List available tools"""
        response = await self.session.post(
            self.base_url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            json={
                "jsonrpc": "2.0",
                "id": "2", 
                "method": "tools/list",
                "params": {}
            }
        )
        result = response.json()
        print("🔧 Available tools:")
        print(json.dumps(result, indent=2))
        return result
        
    async def get_weather(self, city: str):
        """Get weather forecast for a city"""
        response = await self.session.post(
            self.base_url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            json={
                "jsonrpc": "2.0",
                "id": "3",
                "method": "tools/call",
                "params": {
                    "name": "get_forecast",
                    "arguments": {
                        "city": city
                    }
                }
            }
        )
        result = response.json()
        print(f"🌤️  Weather forecast for {city}:")
        print(json.dumps(result, indent=2))
        return result
        
    async def list_resources(self):
        """List available resources"""
        response = await self.session.post(
            self.base_url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            json={
                "jsonrpc": "2.0",
                "id": "4",
                "method": "resources/list", 
                "params": {}
            }
        )
        result = response.json()
        print("📦 Available resources:")
        print(json.dumps(result, indent=2))
        return result
        
    async def get_closet(self):
        """Get closet inventory"""
        response = await self.session.post(
            self.base_url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            json={
                "jsonrpc": "2.0",
                "id": "5",
                "method": "resources/read",
                "params": {
                    "uri": "my-closet://"
                }
            }
        )
        result = response.json()
        print("👕 Closet inventory:")
        print(json.dumps(result, indent=2))
        return result
        
    async def close(self):
        """Close the client session"""
        await self.session.aclose()

async def main():
    """Main example flow"""
    # Get APIM URL from environment or use default
    apim_url = os.getenv("MCP_WEATHER_API_URL", "https://your-apim-service.azure-api.net/mcp-weather/mcp")
    
    if "your-apim-service" in apim_url:
        print("❌ Please set the MCP_WEATHER_API_URL environment variable with your actual APIM URL")
        print("   You can find this URL in the output of `azd up` command")
        print("   Example: export MCP_WEATHER_API_URL=https://apim-abc123.azure-api.net/mcp-weather/mcp")
        sys.exit(1)
        
    print(f"🚀 Connecting to MCP server via APIM: {apim_url}")
    
    client = MCPClient(apim_url)
    
    try:
        # Initialize session
        await client.initialize()
        print()
        
        # List available tools
        await client.list_tools()
        print()
        
        # Get weather for a city
        city = "London"
        await client.get_weather(city)
        print()
        
        # List resources
        await client.list_resources()
        print()
        
        # Get closet inventory
        await client.get_closet()
        print()
        
        print("✅ All operations completed successfully!")
        
    except httpx.HTTPError as e:
        print(f"❌ HTTP error: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    print("🌤️  MCP Weather Client via Azure APIM")
    print("=" * 50)
    asyncio.run(main())