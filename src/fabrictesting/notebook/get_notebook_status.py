import time

import requests


def handle_successful_response(response: requests.Response) -> dict:
    """
    Processes the successful response (status code 200) from the API.

    Args:
        response (requests.Response): The API response.

    Returns:
        dict: Dictionary containing the response status
        and content if job completes or fails.
    """
    response_data = response.json()
    job_status = response_data.get("status")

    if job_status is None:
        raise Exception("There was no job_status in the fetch url response")

    if job_status == "Completed":
        print("Notebook job completed successfully.")
        return {"status_code": response.status_code, "content": response.content}

    elif job_status == "Failed":
        return handle_failed_job(response_data, response)

    else:
        print("Notebook job is still in progress...")
        return None  # Job still running


def handle_failed_job(response_data: dict, response: requests.Response) -> dict:
    """
    Processes the failure response if the job status is "Failed".

    Args:
        response_data (dict): The parsed response data from the API.
        response (requests.Response): The original response.

    Returns:
        dict: The status and content if the job failed due to unknown reasons.
    """
    response_failure_reason = response_data.get("failureReason")

    if response_failure_reason is None:
        raise Exception("There was no failure reason in the fetch url response")

    response_message = response_failure_reason.get("message")

    if response_message is None:
        raise Exception("There was no message in the fetch url response")

    if "No notebook execution state found" in response_message:
        print("No execution state found, retrying...")
    else:
        print("Failure reason unknown, returning...")
        print(f"Status code: {response.status_code}")
        print(f"Content: {str(response.content)}")
        return {"status_code": response.status_code, "content": response.content}

    return None  # To signify retry


def handle_non_successful_response(response: requests.Response) -> dict:
    """
    Handles responses where the status code is not 200 or 202.

    Args:
        response (requests.Response): The API response.

    Returns:
        dict: The status and content when an unexpected status code is encountered.
    """
    if response.status_code == 202:
        print("Job still running, retrying...")
        return None  # Job still running

    print(
        f"Unexpected status code: {response.status_code}. Response: {response.content}"
    )
    return {"status_code": response.status_code, "content": response.content}


def poll_notebook_run_status(
    *, fetch_url: str, retry_after: int, token_string: str
) -> dict:
    """
    Polls the notebook run status at the given URL until the job completes.

    Args:
        fetch_url (str): The URL to poll for the job status.
        https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/jobs/instances/{jobInstanceId}
        retry_after (int): The time to wait (in seconds) between polling attempts.
        token_string (str): The authorization token for the API.

    Returns:
        dict: The final status of the notebook job.

    Todo:
        Implement functionality to avoid infinity loop

    """
    headers = {"Authorization": f"Bearer {token_string}"}

    while True:
        response = requests.get(fetch_url, headers=headers)

        if response.status_code == 200:
            result = handle_successful_response(response)
            if result is not None:
                return result

        else:
            result = handle_non_successful_response(response)
            if result is not None:
                return result

        # Wait for the specified retry time before polling again
        time.sleep(retry_after)
