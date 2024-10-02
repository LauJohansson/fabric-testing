# fabric-testing
**Author: Lau Johansson**

This library enables you to deploy python test to Microsoft Fabric.
With this CLI, it is possible to test functionalities like `CREATE TABLE` or `MERGE INTO`.

## Usage

Deploy python tests to Fabric:
```powershell
fabric-testing-submit `
    --tests-path <path> `
    --whl-path <path> ` #(optional)
    --requirements-file <path> ` #(optional)
    --workspace-name <name> `
    --workspace-id <id> `
    --lakehouse-name <name> `
    --lakehouse-id <id>
```

Fetch the notebook status from Fabric:
```powershell
fabric-testing-fetch `
    --tenant-id <your-tenant-id> `
    --url <your-fetch-url>

# or if you want to use logged fetch url
fabric-testing-fetch `
    --tenant-id <your-tenant-id> `
    --fetch-url-log-file-path <path-to-log-file>
```

The interaction with OneLake use default azure login settings. 
Therefore, remember to login to the expected user (or spn):

```powershell
az login --tenant <tenant-id>
```

## Authentication support

### Fetch
Fetch should be fully supported both User and Service Principal

### Submit
Submit is only fully supported for User.

Currently the Job scheduler API only support `User` identity.

Fabric-testing library are expected to work for service principals
when these APIs support the identity. See the documentation:

* https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/get-item-job-instance?tabs=HTTP
* https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/get-item-schedule?tabs=HTTP

## Requirements
* Ensure your Fabric capacity is turned on
* Align the environment (python version) with the python version of your custom wheel
* User or service principal needs at the right level of access to the Fabric workspace
  * Needs access to onelake
  * Needs access to create and run notebooks
  * If your tests require other permissions, of course, give the permission to the SPN


# Limitations and known issues

* Ensure that the lakehouse for the test-upload (OneLake) in the same workspace as where you execute the notebook runs
* Referencing between test-files will cause import errors


# Future improvements

* Automatically extracts workspaceId and lakehouseId, so the user only needs to add names
* If the [create notebook API](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/create-notebook?tabs=HTTP) supports uploading a base64 encoded .py file, intead of uploading .ipynb files - that could perhaps be preferable.
* 