# MCP-DEMO

## Demos

Using [Python SDK for Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk)

## 0. Local MCP Weather

This also works in GitHub Codespaces.

```bash
cd demos/0-local-mcp-weather
pip install uv
uv init
uv add "mcp[cli]"

uv run weather.py

# MCP Inspector
uv run mcp dev weather.py
# Command: uv
# Arguments: run weather.py || run --with mcp mcp run demos/0-local-mcp-weather/weather.py
```

## 1. Remote MCP Weather

Based on:

- [Mossaka/remote-mcp-python-demo](https://github.com/Mossaka/remote-mcp-python-demo)
- [Google Build and deploy a remote MCP server on Cloud Run](https://cloud.google.com/run/docs/tutorials/deploy-remote-mcp-server)
- [jlowin/fastmcp samples](https://github.com/jlowin/fastmcp)

### Build the MCP server

```powershell
# Navigate to the infra folder
cd demos/1-remote-mcp-weather

# Install UV if not already installed
pip install uv

# Initialize UV and add MCP CLI
uv init

# Add MCP with CLI support
uv add "mcp[cli]"
```

### Deploy the Azure Container App

Note that Docker Desktop must be running to be able to build the container image.

```powershell
# Install Azure Developer CLI (azd)
winget install microsoft.azd

# Login to Azure
azd auth login

# Initialize the Azure Developer project
azd init --from-code
# > Scan current directory
# > What is the name of your project? infra

# Provision and deploy everything
azd up
# > Enter a unique environment name: mcp
# > Select an Azure Subscription to use: Subscription Name
# > Enter a value for the 'location' infrastructure parameter: 39. (Europe) West Europe (westeurope)

# Deleting all resources and deployed code on Azure
azd down
```

## 2. Remote MCP Weather with Azure API Management

Based on [Azure-Samples/remote-mcp-apim-functions-python](https://github.com/Azure-Samples/remote-mcp-apim-functions-python)

The APIM integration provides centralized API management, enhanced security, monitoring, and easier scaling for the MCP weather server.

### Features

- **MCP Protocol Support**: Full support for MCP StreamableHTTP transport
- **Weather Forecasting**: Get weather forecasts for any city using Open-Meteo API
- **Clothing Recommendations**: AI-powered clothing suggestions based on weather
- **Virtual Closet**: Access to a comprehensive clothing inventory resource
- **API Management**: Rate limiting, CORS, authentication, and monitoring via Azure APIM

### Deployment

The APIM integration is included in the same infrastructure as the regular remote MCP weather demo. When you run `azd up` from the `demos/1-remote-mcp-weather` directory, it will deploy:

1. **Container App**: The MCP weather server
2. **APIM Service**: Azure API Management service (Consumption tier)
3. **MCP Weather API**: The weather server exposed through APIM with proper policies

### Usage

After deployment, you'll get output variables including:
- `APIM_GATEWAY_URL`: The APIM gateway base URL
- `MCP_WEATHER_API_URL`: Direct URL to the MCP endpoint via APIM

#### Example MCP Client Usage

```bash
# Initialize MCP session via APIM
curl -X POST "${MCP_WEATHER_API_URL}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {
        "name": "weather-client",
        "version": "1.0.0"
      }
    }
  }'

# List available tools
curl -X POST "${MCP_WEATHER_API_URL}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": "2",
    "method": "tools/list",
    "params": {}
  }'

# Get weather forecast for London
curl -X POST "${MCP_WEATHER_API_URL}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": "3",
    "method": "tools/call",
    "params": {
      "name": "get_forecast",
      "arguments": {
        "city": "London"
      }
    }
  }'
```

#### Available Tools

- `add_test(a: int, b: int)`: Simple addition for testing
- `get_forecast(city: str)`: Get weather forecast for a city

#### Available Resources

- `greeting://{name}`: Get personalized greetings
- `my-closet://`: Access virtual clothing inventory

#### Available Prompts

- `run_cloths_recommendation(day: str, city: str)`: Generate clothing recommendations

### APIM Features

The APIM integration includes:

- **CORS Support**: Cross-origin requests enabled for browser clients
- **Header Management**: Automatic MCP protocol header handling
- **Retry Logic**: Automatic retries for backend failures
- **Error Handling**: Structured error responses and logging
- **Monitoring**: Built-in Azure Monitor integration
- **Rate Limiting**: Configurable via APIM policies (can be added as needed)

### Architecture

```
Client → APIM Gateway → Container App (MCP Server) → Open-Meteo API
```

The APIM service acts as a gateway, providing enterprise-grade API management features while maintaining full compatibility with the MCP protocol.
