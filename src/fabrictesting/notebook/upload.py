import json
import time

import requests

from fabrictesting.notebook.create import (
    convert_notebook_into_inlinebase64,
    convert_platform_into_inlinebase64,
)


def upload_notebook(
    *,
    display_name: str,
    description: str,
    notebook_definition: str,
    platform_definition: str,
    workspace_id: str,
    token_string: str,
):
    """

    https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/create-notebook?tabs=HTTP

    """
    print("Prepare uploading notebook...")
    print(f"    Display Name: {display_name}")
    print(f"    To workspace with id: {workspace_id}")

    print("Converting notebook payload to base64...")
    _notebook_payload = convert_notebook_into_inlinebase64(notebook_definition)

    print("Converting platform payload to base64...")
    _platform_payload = convert_platform_into_inlinebase64(platform_definition)

    data = {
        "displayName": display_name,
        "description": description,
        "definition": {
            "format": "ipynb",
            "parts": [
                {
                    "path": "artifact.content.ipynb",
                    "payload": _notebook_payload,
                    "payloadType": "InlineBase64",
                },
                {
                    "path": ".platform",
                    "payload": _platform_payload,
                    "payloadType": "InlineBase64",
                },
            ],
        },
    }

    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_string}",
    }

    print("Posting notebook...")
    response = requests.post(
        url=f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/notebooks",
        headers=header,
        data=json.dumps(data),
    )
    print("Posting finished!")

    if response.status_code == 201:
        print("Notebook was successfully created!")
    elif response.status_code == 202:
        print("Notebook Request accepted, notebook provisioning in progress...")
        # Extract Location header to check the notebook status

        location_url = response.headers.get("Location")
        retry_after = int(
            response.headers.get("Retry-After", 20)
        )  # Default to 20 seconds if not provided

        if location_url:
            print(f"To check the status, polling the following URL: {location_url}")

            response_poll = poll_notebook_upload_status(
                location_url, retry_after, token_string
            )
            return {
                "status_code": response_poll.status_code,
                "content": response_poll.content,
            }
        else:
            print("No Location header found in the response. Continues...")
    else:
        raise Exception(
            f"Notebook upload failed with status code {response.status_code}"
            f"\n"
            f"Content: {response.content}"
        )

    return {"status_code": response.status_code, "content": response.content}


def poll_notebook_upload_status(location_url: str, retry_after: int, token_string: str):
    """Polls the notebook creation status until it's completed."""

    def _retrieve_percent_complete(response_content: bytes):
        response_json = json.loads(response_content)
        _percent_complete = response_json.get("percentComplete", None)

        if _percent_complete is None:
            return "0"
        return str(_percent_complete)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_string}",
    }

    while True:
        response = requests.get(location_url, headers=headers)
        percent_complete = _retrieve_percent_complete(response.content)

        if percent_complete != "100":
            print(f"Notebook creation is at {percent_complete}/100 %...")
            print(f"Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
        elif response.status_code == 200:
            print(f"Notebook creation is at {percent_complete}/100 %!")
            print("Notebook creation completed.")
            return response
        elif response.status_code == 202:
            print(f"Notebook creation is at {percent_complete} percent...")
            print("Notebook creation still in progress...")

            # Wait for the recommended time before retrying
            print(f"Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
        else:
            print(
                f"Unexpected status code: {response.status_code},"
                f" details: {response.content}"
            )
            break
