

# OneLake
Microsoft provides [documentation on how to use python for OneLake - se more [here](https://learn.microsoft.com/en-us/fabric/onelake/onelake-access-python).

Two PyPI libraries is necessary ``azure-storage-file-datalake`` and ``azure-identity``.

## Authentication
### DefaultAzureCredential
To authenticate to OneLake, we use the DefaultAzureCredential to automatically detect credentials 
and obtain the correct authentication token. 
Common methods of providing credentials for the Azure SDK include using the ``az login`` command 
in the Azure Command Line Interface or the ``Connect-AzAccount`` cmdlet from Azure PowerShell.

[Documentation](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python)

## Working with files

### filedatalake Package

FileSystemClient: </br>
A client to interact with a specific file system, even if that file system may not yet exist.


The ``get_file_client()`` is used for retrieving the file client.

The ``upload_data()`` method is applied for uploading data to OneLake. 

[Documentation](https://learn.microsoft.com/en-us/python/api/azure-storage-file-datalake/azure.storage.filedatalake?view=azure-python)



