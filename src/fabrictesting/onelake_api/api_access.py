import os
from azure.storage.filedatalake import (
    DataLakeServiceClient,
    DataLakeDirectoryClient,
    FileSystemClient
)
from azure.identity import DefaultAzureCredential
def get_service_client() -> DataLakeServiceClient:
    """
    https://learn.microsoft.com/en-us/fabric/onelake/onelake-access-python

    """
    account_url = f"https://onelake.dfs.fabric.microsoft.com"
    token_credential = DefaultAzureCredential()

    service_client = DataLakeServiceClient(account_url, credential=token_credential)

    return service_client