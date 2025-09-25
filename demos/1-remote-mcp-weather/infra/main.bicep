targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment that can be used as part of naming resource convention')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

param mcpContainerPyExists bool

// Tags that should be applied to all resources.
// 
// Note that 'azd-service-name' tags should be applied separately to service host resources.
// Example usage:
//   tags: union(tags, { 'azd-service-name': <service name in azure.yaml> })
var tags = {
  'azd-env-name': environmentName
}

// Organize resources in a resource group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: 'rg-${environmentName}'
  location: location
  tags: tags
}

module resources 'resources.bicep' = {
  scope: rg
  name: 'resources'
  params: {
    location: location
    tags: tags
    mcpContainerPyExists: mcpContainerPyExists
  }
}

// ------------------
//    OUTPUT
// ------------------
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = resources.outputs.AZURE_CONTAINER_REGISTRY_ENDPOINT
output AZURE_RESOURCE_MCP_CONTAINER_PY_ID string = resources.outputs.AZURE_RESOURCE_MCP_CONTAINER_PY_ID
output APIM_SERVICE_NAME string = resources.outputs.APIM_SERVICE_NAME
output APIM_GATEWAY_URL string = resources.outputs.APIM_GATEWAY_URL
output MCP_WEATHER_API_URL string = resources.outputs.MCP_WEATHER_API_URL
