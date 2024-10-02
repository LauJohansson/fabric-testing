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
    Uploads a notebook to a specified workspace in the Fabric API.

    This function prepares and uploads a notebook by converting the notebook
     and platform definitions into base64-encoded format. It sends a POST request
     to the Fabric API to create a notebook within the specified
    workspace. If the notebook upload is accepted for provisioning (HTTP 202),
    it polls the notebook creation status until it completes.

    Args:
        display_name (str): The display name of the notebook.
        description (str): A brief description of the notebook.
        notebook_definition (str): The notebook definition content in JSON format.
        platform_definition (str): The platform definition content in JSON format.
        workspace_id (str): The ID of the workspace where the notebook is uploaded.
        token_string (str): The bearer token used to authenticate the API request.

    Returns:
        dict: A dictionary containing the status code and response
            content of the API request, or the result of polling the
            upload status if the notebook provisioning is in progress.

    Raises:
        Exception: If the notebook upload fails with a status code
                    other than 201 or 202.

    See Also:
        Fabric API documentation: https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/create-notebook?tabs=HTTP
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
    """
    Polls the status of a notebook creation until it is completed or fails.

    This function sends repeated GET requests to a given location URL to check
    the progress of the notebook creation. The polling is done at intervals
    specified by the `Retry-After` header (or a default interval).
    The function will continue to poll until the creation reaches 100% completion.

    Args:
        location_url (str):
            The URL from which to fetch the status of the notebook creation.
        retry_after (int):
            The number of seconds to wait between polling attempts.
        token_string (str):
            The bearer token used to authenticate the API request.

    Returns:
        requests.Response: The final response object once
                            the notebook creation is complete.

    Raises:
        Exception: If the API returns unexpected status
                codes or an error occurs during polling.
    """

    def _retrieve_percent_complete(response_content: bytes):
        try:
            response_json = json.loads(response_content)
            _percent_complete = response_json.get("percentComplete", None)

            if _percent_complete is None:
                return "0"
            return str(_percent_complete)
        except json.JSONDecodeError:
            # Handle non-JSON responses like errors
            print("Could not retrieve percenComplete value. Continues...")
            return None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_string}",
    }

    while True:
        response = requests.get(location_url, headers=headers)
        if response.status_code in [200, 202]:
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
        else:
            # For unexpected status codes, return the response and break the loop
            print(
                f"Unexpected status code: {response.status_code}, "
                f"details: {response.content}"
            )
            return response  # Ensures the loop is exited for unexpected status codes
