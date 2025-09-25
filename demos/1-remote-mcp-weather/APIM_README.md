# MCP Weather Server with Azure API Management

This demo implements a Model Context Protocol (MCP) server for weather forecasting, deployed on Azure Container Apps and exposed through Azure API Management (APIM).

## Architecture

```
Client → Azure APIM → Container App (MCP Server) → Open-Meteo API
```

## Features

### MCP Protocol Support
- Full MCP 2024-11-05 protocol implementation
- StreamableHTTP transport
- Tools, resources, and prompts support

### Weather & Lifestyle Tools
- **Weather Forecasting**: Get detailed weather forecasts for any city
- **Clothing Recommendations**: AI-powered outfit suggestions based on weather
- **Virtual Closet**: Comprehensive clothing inventory management

### APIM Integration Benefits
- **Security**: API key authentication and CORS support
- **Reliability**: Retry policies and error handling
- **Monitoring**: Built-in Azure Monitor integration
- **Scalability**: Azure's global infrastructure

## Deployment

### Prerequisites
- Azure subscription
- Docker Desktop (for container builds)
- Azure Developer CLI (`azd`)

### Deploy Infrastructure

```bash
# Navigate to the demo directory
cd demos/1-remote-mcp-weather

# Install Azure Developer CLI
winget install microsoft.azd  # Windows
brew install azure/azd/azd    # macOS

# Login to Azure
azd auth login

# Deploy everything
azd up
# Follow prompts for environment name, subscription, and region
```

The deployment creates:
- **Resource Group**: Contains all resources
- **Container Registry**: For the MCP server container
- **Container App**: Hosts the MCP weather server
- **APIM Service**: API Management gateway (Consumption tier)
- **MCP Weather API**: The weather server exposed via APIM
- **Application Insights**: Monitoring and logging

### Output Variables

After successful deployment:
- `APIM_GATEWAY_URL`: Base URL for the APIM service
- `MCP_WEATHER_API_URL`: Direct URL to the MCP endpoint

## Usage

### Using the Example Client

```bash
# Set the API URL from deployment output
export MCP_WEATHER_API_URL="https://apim-xxxxx.azure-api.net/mcp-weather/mcp"

# Install dependencies
pip install httpx

# Run the example client
python example_client.py
```

### Manual API Testing

#### Initialize MCP Session
```bash
curl -X POST "$MCP_WEATHER_API_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "test-client", "version": "1.0.0"}
    }
  }'
```

#### List Available Tools
```bash
curl -X POST "$MCP_WEATHER_API_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": "2",
    "method": "tools/list",
    "params": {}
  }'
```

#### Get Weather Forecast
```bash
curl -X POST "$MCP_WEATHER_API_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0", 
    "id": "3",
    "method": "tools/call",
    "params": {
      "name": "get_forecast",
      "arguments": {"city": "Paris"}
    }
  }'
```

## Available Endpoints

### Tools
- `add_test(a: int, b: int)`: Simple addition for testing
- `get_forecast(city: str)`: Weather forecast for specified city

### Resources  
- `greeting://{name}`: Personalized greeting messages
- `my-closet://`: Virtual clothing inventory

### Prompts
- `run_cloths_recommendation(day: str, city: str)`: Clothing suggestions

## APIM Policies

The APIM configuration includes:

### Inbound Policies
- **Header Management**: Automatic MCP protocol headers
- **CORS**: Cross-origin request support
- **Content-Type**: Ensures proper JSON content type

### Backend Policies  
- **Retry Logic**: Automatic retries for 5xx errors (3 attempts)

### Outbound Policies
- **Custom Headers**: Adds MCP server identification

### Error Handling
- **Logging**: Structured error logging for debugging
- **Error Responses**: Consistent error format

## Monitoring

The deployment includes Azure Application Insights for:
- **Request Tracing**: Full request/response logging
- **Performance Metrics**: Response times and throughput
- **Error Analytics**: Failure analysis and debugging
- **Custom Telemetry**: MCP-specific metrics

Access monitoring data through:
1. Azure Portal → Application Insights
2. APIM Analytics blade
3. Container App logs

## Development

### Local Testing
```bash
# Run the MCP server locally
uv run weather.py

# Test direct connection (bypassing APIM)
curl -X POST "http://localhost:8000/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}'
```

### Customization

#### Adding New Tools
1. Add tool functions to `weather.py` using `@mcp.tool()` decorator
2. Update OpenAPI spec in `infra/apim-api/openapi.json`
3. Redeploy with `azd up`

#### Modifying APIM Policies
1. Edit `infra/apim-api/policy.xml`
2. Redeploy infrastructure

## Cleanup

```bash
# Remove all Azure resources
azd down
```

## Troubleshooting

### Common Issues

**APIM Gateway URL not resolving**
- Check APIM service status in Azure Portal
- Verify DNS propagation (can take a few minutes)

**MCP Protocol Errors**
- Ensure all required headers are present
- Check Content-Type is `application/json`
- Verify Accept header includes `text/event-stream`

**Container App not responding**
- Check container logs in Azure Portal
- Verify application startup in Container Apps console

### Debugging Tools

1. **Azure Portal**: Full resource visibility
2. **Application Insights**: Request tracing and performance
3. **APIM Test Console**: Built-in API testing
4. **Container App Console**: Direct container access

## References

- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [Azure API Management Documentation](https://docs.microsoft.com/azure/api-management/)
- [Azure Container Apps Documentation](https://docs.microsoft.com/azure/container-apps/)