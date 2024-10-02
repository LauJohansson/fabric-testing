import json

import requests


def list_notebooks(*, workspace_id: str, token_string: str):
    """

    :return:


    https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/list-notebooks?tabs=HTTP
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
    response_json = json.loads(response.content)

    workspaces_dict = {
        workspace["displayName"]: workspace["id"]
        for workspace in response_json.get("value", [])
        if "displayName" in workspace and "id" in workspace
    }
    return workspaces_dict


def get_notebook_id(*, notebook_name: str, workspace_id: str, token_string):
    workspaces_dict = list_notebooks(
        workspace_id=workspace_id, token_string=token_string
    )

    try:
        return workspaces_dict[notebook_name]

    except KeyError:
        raise Exception(
            f"The notebook {notebook_name} was not found in the workspace {workspace_id}"
        )
