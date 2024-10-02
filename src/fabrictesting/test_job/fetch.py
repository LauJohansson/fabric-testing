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
