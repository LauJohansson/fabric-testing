from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import (
    DataLakeServiceClient,
)


def get_service_client() -> DataLakeServiceClient:
    """
    https://learn.microsoft.com/en-us/fabric/onelake/onelake-access-python

    """
    account_url = "https://onelake.dfs.fabric.microsoft.com"
    token_credential = DefaultAzureCredential()

    service_client = DataLakeServiceClient(account_url, credential=token_credential)

    return service_client
