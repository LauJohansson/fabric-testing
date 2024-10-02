from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import (
    DataLakeServiceClient,
)


def get_service_client() -> DataLakeServiceClient:
    """
    Creates and returns an authenticated DataLakeServiceClient
    for accessing OneLake.

    This function uses the `DefaultAzureCredential` to authenticate with Azure and
    returns a `DataLakeServiceClient` object, which can be used to interact with
    OneLake's Data Lake storage.

    Returns:
        DataLakeServiceClient: An authenticated client for interacting
        with Azure Data Lake Storage.

    See Also:
        OneLake Access Documentation:
        https://learn.microsoft.com/en-us/fabric/onelake/onelake-access-python
    """
    account_url = "https://onelake.dfs.fabric.microsoft.com"
    token_credential = DefaultAzureCredential()

    service_client = DataLakeServiceClient(account_url, credential=token_credential)

    return service_client
