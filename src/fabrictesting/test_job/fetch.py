import argparse

from fabrictesting.fabric_api.api_access import (
    get_client_fabric_token,
    get_personal_fabric_token,
)
from fabrictesting.notebook.get_notebook_status import poll_notebook_run_status
from fabrictesting.utilities.load_fetch_url_log import load_fetch_url
from fabrictesting.utilities.validate_args import validate_args


def fetch_args():
    parser = argparse.ArgumentParser(description="Fetch test from Microsoft Fabric")

    parser.add_argument(
        "--service-principal",
        type=bool,
        required=False,
        help="Run as a Service Principal",
    )
    parser.add_argument(
        "--tenant-id", type=str, required=True, help="The Azure tenant ID"
    )

    parser.add_argument(
        "--client-id", type=str, required=False, help="The Azure client ID"
    )
    parser.add_argument(
        "--client-secret", type=str, required=False, help="The Azure client secret"
    )

    parser.add_argument(
        "--retry-after",
        type=int,
        default=60,
        required=False,
        help="Define the frequency of the re-fetching",
    )

    # Create a mutually exclusive group for --fetch-url-log-file-path and --url
    fetch_url_group = parser.add_mutually_exclusive_group(required=True)

    fetch_url_group.add_argument(
        "--fetch-url-log-file-path",
        type=str,
        help="The path to the logged fetch url",
    )

    fetch_url_group.add_argument(
        "--url",
        type=str,
        help="Fetch url",
    )

    args = parser.parse_args()

    validate_args(args, parser)

    return args


def fetch(args):
    """
    Command-line utility to fetch test results from Microsoft Fabric.

    This CLI tool is designed to fetch the status or results of tests
    run on Microsoft Fabric notebooks. The tool supports two modes of authentication:
    using a service principal or a personal user token.
    It polls the status of a notebook run by calling the appropriate Fabric API.

    The tool provides an option to specify a URL directly or
    load the fetch URL from a log file.

    Arguments:
        --service-principal (bool, optional):
            If provided, the tool authenticates using service principal credentials.
        --tenant-id (str, required): The Azure tenant ID for authentication.
        --client-id (str, optional):
            The Azure client ID for the service principal
            (required if using service principal authentication).
        --client-secret (str, optional):
            The Azure client secret for the service principal
            (required if using service principal authentication).
        --retry-after (int, optional):
            Defines how often to poll the status of the notebook run.
            Default is 60 seconds.

        --fetch-url-log-file-path (str, optional, mutually exclusive with --url):
            The path to a log file containing the fetch URL.
        --url (str, optional, mutually exclusive with --fetch-url-log-file-path):
            The URL used to fetch the status or results directly.

    Usage:
        To run the tool using a service principal:
            fabric-testing-fetch
                --service-principal True
                --tenant-id <tenant_id>
                --client-id <client_id>
                --client-secret <client_secret>
                --fetch-url-log-file-path <path_to_log_file>

        To run the tool using a personal token:
            fabric-testing-fetch --tenant-id <tenant_id> --url <fetch_url>

    Raises:
        RuntimeError: If argument validation fails or the API polling encounters issues.

    Notes:
        - The `fetch_url` parameter can be provided
            either directly or loaded from a log file.
        - The CLI uses `argparse` for argument parsing and validation.
        - Polling frequency can be customized using the `--retry-after` argument.
    """

    if args.service_principal:
        _fabric_token = get_client_fabric_token(
            args.tenant_id, args.client_id, args.client_secret
        )
    else:
        _fabric_token = get_personal_fabric_token(args.tenant_id)

    _fetch_url = args.url or load_fetch_url(args.fetch_url_log_file_path)

    poll_notebook_run_status(
        fetch_url=_fetch_url, retry_after=args.retry_after, token_string=_fabric_token
    )


def main():
    args = fetch_args()
    fetch(args)


if __name__ == "__main__":
    main()
