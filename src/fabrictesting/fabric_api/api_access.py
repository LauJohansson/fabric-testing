from azure.identity import ClientSecretCredential, InteractiveBrowserCredential


def get_personal_fabric_token(tenant_id: str = None) -> str:
    """
    Retrieves an OAuth 2.0 access token using Azure's InteractiveBrowserCredential.

    This function authenticates a user via a browser and
    retrieves an access token for the Fabric API.
    It accepts an optional tenant ID parameter
    The token is returned for use in authenticated API requests.
    If no token is retrieved, an exception is raised.

    Args:
        tenant_id (str, optional): The Azure tenant ID.


    Returns:
        str: The access token string for authenticated requests.

    Raises:
        Exception: If the token string is None.
    """

    # Tenant ID and scope
    tenant_id = tenant_id  # Your tenant ID
    scope = "https://api.fabric.microsoft.com/.default"

    # Create an InteractiveBrowserCredential object
    interactive_browser_credential = InteractiveBrowserCredential(tenant_id=tenant_id)

    # Get the access token
    access_token = interactive_browser_credential.get_token(scope)
    token_string = access_token.token

    # You can now use token_string for authenticated API requests
    # print(token_string)

    if not token_string:
        raise Exception("Token string was none")

    return token_string


def get_client_fabric_token(tenant_id: str, client_id: str, client_secret: str) -> str:
    """
    Retrieves an OAuth 2.0 access token
    from Azure AD for the specified client credentials.

    This function uses the Azure Identity ClientSecretCredential to authenticate with
    Azure Active Directory (AD) and obtain an access token that can be used to access
    the Fabric API.

    Args:
        tenant_id (str): The Azure AD tenant (directory) ID.
        client_id (str): The client (application) ID registered in Azure AD.
        client_secret (str): The client secret associated with the application.

    Returns:
        str: The access token retrieved from Azure AD to authenticate API requests.

    Raises:
        Exception: If the token string is None, an exception is raised.
    """

    scope = "https://api.fabric.microsoft.com/.default"
    client_secret_credential_class = ClientSecretCredential(
        tenant_id=tenant_id, client_id=client_id, client_secret=client_secret
    )
    access_token_class = client_secret_credential_class.get_token(scope)
    token_string = access_token_class.token

    if not token_string:
        raise Exception("Token string was none")

    return token_string
