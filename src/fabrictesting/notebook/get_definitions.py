import json

import requests


def list_notebooks(*, workspace_id: str, token_string: str):
    """
    Lists all notebooks within a specific workspace by calling the Fabric API.

    This function sends an authenticated GET request to the Fabric API to retrieve
    a list of notebooks within the given workspace.
    It extracts and returns a dictionary that maps notebook display names
    to their corresponding IDs.

    Args:
        workspace_id (str): The ID of the workspace from which to list notebooks.
        token_string (str): The bearer token used for authenticating the API request.

    Returns:
        dict: A dictionary where the keys are notebook display names
                and the values are their IDs.

    Raises:
        Exception: If the API call fails or if the response status is not 200.

    See Also:
        Fabric API documentation: https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/list-notebooks?tabs=HTTP
    """

    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_string}",
    }

    print("Get notebook definitions...")
    response = requests.get(
        url=f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/notebooks",
        headers=header,
    )

    # Raise an exception if the API call fails (non-2xx status code)
    if response.status_code != 200:
        raise Exception(
            f"API call failed with status "
            f"{response.status_code}: {response.content.decode('utf-8')}"
        )

    response_json = json.loads(response.content)

    workspaces_dict = {
        workspace["displayName"]: workspace["id"]
        for workspace in response_json.get("value", [])
        if "displayName" in workspace and "id" in workspace
    }
    return workspaces_dict


def get_notebook_id(*, notebook_name: str, workspace_id: str, token_string):
    """
    Retrieves the ID of a specific notebook by name within a given workspace.

    This function calls `list_notebooks` to get all available notebooks
    in the specified workspace, then attempts to return the ID of the notebook
    with the given name. If the notebook is not found, an exception is raised.

    Args:
        notebook_name (str): The name of the notebook to search for.
        workspace_id (str): The ID of the workspace where the notebook is located.
        token_string (str): The bearer token used for authenticating the API request.

    Returns:
        str: The ID of the notebook if found.

    Raises:
        Exception: If the notebook is not found in the workspace.
    """
    workspaces_dict = list_notebooks(
        workspace_id=workspace_id, token_string=token_string
    )

    try:
        return workspaces_dict[notebook_name]

    except KeyError:
        raise Exception(
            f"The notebook {notebook_name} was not found "
            f"in the workspace {workspace_id}"
        )
