import requests


def run_notebook(
    *,
    item_id: str,
    workspace_id: str,
    token_string: str,
    job_type: str = "RunNotebook",
):
    """
    Triggers the execution of a notebook in a specified workspace using the Fabric API.

    This function sends an authenticated POST request to the Fabric API to trigger
    the execution of a notebook (or similar item) on demand.
    It expects the workspace and item IDs, along with an optional job type. Upon
    successful submission of the job, the API responds with a `Location` header
    containing a URL to fetch the status of the job and a `Retry-After`
    header specifying when to check back for the job status.


    Args:
        item_id (str): The ID of the notebook (or item) to be run.
        workspace_id (str): The ID of the workspace where the notebook resides.
        token_string (str): The bearer token used to authenticate the API request.
        job_type (str, optional): The type of job to trigger. Defaults to "RunNotebook".

    Returns:
        dict: A dictionary containing the following information:
            - "status_code" (int): The HTTP status code of the API response.
            - "fetch_url" (str): The URL to fetch the job status
                from (obtained from the `Location` header).
            - "retry_after" (int): The recommended number of seconds
                to wait before fetching the job status
                (obtained from the `Retry-After` header,
                default is 60 seconds if not provided).

    Raises:
        Exception: If the API call fails with a status code other than 202 (Accepted),
        an exception is raised with the error message.

    See Also:
        Fabric API documentation: https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/run-on-demand-item-job?tabs=HTTP
    """

    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_string}",
    }

    print("Trigger notebook...")
    response = requests.post(
        url=f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/jobs/instances?jobType={job_type}",
        headers=header,
    )

    fetch_url = response.headers.get("Location")
    retry_after = int(response.headers.get("Retry-After", 60))

    status_code = response.status_code

    if status_code != 202:
        raise Exception(
            f"Triggering notebook failed with {status_code}: {str(response.content)}"
        )

    print("Trigger finished!")

    return {
        "status_code": response.status_code,
        "fetch_url": fetch_url,
        "retry_after": retry_after,
    }
