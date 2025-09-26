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
cd demos/2-remote-mcp-weather

# Install UV if not already installed
pip install uv

# Initialize UV and add MCP CLI
uv init

# Add MCP with CLI support
uv add "mcp[cli]"
```

### Deploy the Azure Container App

Note that Dcoker Desktop must be running to be able to build the container image.

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

```powershell
npx @modelcontextprotocol/inspector https://mcp-container-py.victoriousriver-c8c0c9c5.westeurope.azurecontainerapps.io/mcp
```

## 3. Remote MCP Weather with Azure API Management

Based on [Azure-Samples/remote-mcp-apim-functions-python](https://github.com/Azure-Samples/remote-mcp-apim-functions-python)
