# Fabric API

## Authentication

The access token is obtained from: https://api.fabric.microsoft.com/.default

The PyPI package ``azure-identity`` provides classes for handling identities.

### User
``InteractiveBrowserCredential`` launches the system default browser to interactively authenticate a user, and obtain an access token.


[Dcoumentation](https://learn.microsoft.com/en-us/dotnet/api/azure.identity.interactivebrowsercredential?view=azure-dotnet)


### Service Principal
``ClientSecretCredential`` enables authentication to Microsoft Entra ID using a client secret that was generated for an App Registration.

[Documentation](https://learn.microsoft.com/en-us/dotnet/api/azure.identity.clientsecretcredential?view=azure-dotnet)

## API methods applied

* [Notebook definitions](https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/notebooks)
* [Job Scheduler - Run On Demand Item Job](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/run-on-demand-item-job?tabs=HTTP)
* [Items - Create Notebook](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/create-notebook?tabs=HTTP)