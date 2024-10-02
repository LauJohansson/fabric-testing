import requests


def run_notebook(
    *,
    item_id: str,
    workspace_id: str,
    token_string: str,
    job_type: str = "RunNotebook",
):
    """

    :return:


    https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/run-on-demand-item-job?tabs=HTTP
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
