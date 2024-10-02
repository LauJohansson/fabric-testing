import argparse
import time

from fabrictesting.fabric_api.api_access import (
    get_client_fabric_token,
    get_personal_fabric_token,
)
from fabrictesting.notebook.create import (
    create_platform_file_content,
    load_default_notebook,
)
from fabrictesting.notebook.get_definitions import get_notebook_id
from fabrictesting.notebook.run import run_notebook
from fabrictesting.notebook.upload import upload_notebook
from fabrictesting.onelake_api.api_file import upload_folder_to_onelake
from fabrictesting.utilities.collect import create_temp_folder_with_files
from fabrictesting.utilities.save_fetch_url_log import save_fetch_url_log
from fabrictesting.utilities.validate_args import validate_args


def submit_args():
    parser = argparse.ArgumentParser(description="Submit tests to Microsoft Fabric")

    parser.add_argument(
        "--tenant-id", type=str, required=True, help="The Azure tenant ID"
    )

    parser.add_argument(
        "--whl-path",
        type=str,
        required=False,
        default=None,
        help="The path to the .whl file to upload",
    )
    parser.add_argument(
        "--tests-path", type=str, required=True, help="The path to the tests to upload"
    )
    parser.add_argument(
        "--requirements-file",
        type=str,
        required=False,
        default=None,
        help="The path to the test requirements.",
    )
    parser.add_argument(
        "--workspace-name",
        type=str,
        required=True,
        help="The name of the Fabric workspace.",
    )
    parser.add_argument(
        "--workspace-id",
        type=str,
        required=True,
        help="The id of the Fabric workspace.",
    )
    parser.add_argument(
        "--lakehouse-name",
        type=str,
        required=True,
        help="The name of the lakehouse",
    )
    parser.add_argument(
        "--lakehouse-id",
        type=str,
        required=True,
        help="The id of the lakehouse",
    )

    parser.add_argument(
        "--output-log-file-path",
        type=str,
        required=False,
        default=None,
        help="The name of the output file",
    )

    parser.add_argument(
        "--service-principal",
        type=bool,
        required=False,
        help="Run as a Service Principal",
    )

    parser.add_argument(
        "--client-id", type=str, required=False, help="The Azure client ID"
    )
    parser.add_argument(
        "--client-secret", type=str, required=False, help="The Azure client secret"
    )

    args = parser.parse_args()

    validate_args(args, parser)

    return args


def submit(args) -> str:
    """
    Submits a set of tests to Microsoft Fabric by uploading test files,
    generating a notebook, and running it.

    This is the core function of the CLI command `fabric-testing-submit` command.
    It performs the following steps:

    1. Creates a temporary folder containing the `.whl` file, tests,
        and requirements file.
    2. Uploads the temporary folder to OneLake DataLake.
    3. Generates a Jupyter notebook to install dependencies,
        load and install custom wheel files, and run the unit tests from OneLake.
    4. Uploads the generated notebook to the specified Fabric workspace.
    5. Retrieves the notebook's unique ID.
    6. Executes the notebook using the Fabric API
        and returns the URL for fetching the results.

    Returns:
        str: The URL to fetch the results of the notebook execution.

    Raises:
        RuntimeError: If any part of the process
        (file upload, notebook creation, notebook execution) fails.


    Usage:
        To submit the tests using a service principal:
            fabric-testing-submit
                --service-principal True
                --tenant-id <tenant_id>
                --client-id <client_id>
                --client-secret <client_secret>
                --whl-path <path_to_wheel_file>
                --tests-path <path_to_tests>
                --requirements-file <path_to_requirements_file>
                --workspace-name <workspace_name>
                --workspace-id <workspace_id>
                --lakehouse-name <lakehouse_name>
                --lakehouse-id <lakehouse_id>
                --output-log-file-path <path_to_log_file>

        To submit the tests using a personal token:
            fabric-testing-submit
                --tenant-id <tenant_id>
                --whl-path <path_to_wheel_file>
                --tests-path <path_to_tests>
                --requirements-file <path_to_requirements_file>
                --workspace-name <workspace_name>
                --workspace-id <workspace_id>
                --lakehouse-name <lakehouse_name>
                --lakehouse-id <lakehouse_id>
                --output-log-file-path <path_to_log_file>

    See Also:
        - `fabric-testing-fetch`:
            CLI command for fetching the status and results of submitted tests.
    """

    print("Starting fabric-testing submit...")

    # 1 Create temp folder with wheel, tests and requirement file
    temp_dir, wheel_name, rqs_name = create_temp_folder_with_files(
        whl_path=args.whl_path,
        tests_path=args.tests_path,
        requirements_file=args.requirements_file,
    )

    # 2 Upload folder to OneLake
    folder_name = upload_folder_to_onelake(
        temp_folder=temp_dir,
        workspace_name=args.workspace_name,
        lakehouse_name=args.lakehouse_name,
    )

    notebook_name = folder_name

    # 3 Generate notebook for that execute tests in Microsoft Fabric
    _notebook_contents = load_default_notebook(
        lakehouse_id=args.lakehouse_id,
        default_lakehouse_name=args.lakehouse_name,
        default_lakehouse_workspace_id=args.workspace_id,
        workspace_name=args.workspace_name,
        submit_folder=folder_name,
        wheel_name=wheel_name,
        requirements_file_name=rqs_name,
        unittest_folder_name="tests",
    )

    _platform_contents = create_platform_file_content(
        display_name=notebook_name, description="This is a fabric-testing notebook"
    )

    # 4a Retrieve token for interaction with Fabric API
    if args.service_principal:
        _fabric_token = get_client_fabric_token(
            args.tenant_id, args.client_id, args.client_secret
        )
    else:
        _fabric_token = get_personal_fabric_token(args.tenant_id)

    # 4b Upload the notebook to Fabric
    upload_notebook(
        display_name=notebook_name,
        description="This is a fabric-testing notebook",
        notebook_definition=_notebook_contents,
        platform_definition=_platform_contents,
        workspace_id=args.workspace_id,
        token_string=_fabric_token,
    )

    print("Give Fabric API 5 seconds to upload notebook...")
    time.sleep(5)

    # 5 Retrieve the notebook id
    notebook_id = get_notebook_id(
        notebook_name=notebook_name,
        workspace_id=args.workspace_id,
        token_string=_fabric_token,
    )

    # 6 Run the notebook
    run_response = run_notebook(
        item_id=notebook_id,
        workspace_id=args.workspace_id,
        token_string=_fabric_token,
    )
    _run_status = run_response["status_code"]
    _fetch_url = run_response["fetch_url"]

    if args.output_log_file_path:
        save_fetch_url_log(_fetch_url)

    print(f"Notebook triggered with status {_run_status}")
    print(f"Notebook has the name: {notebook_name}")
    print(f"Notebook has id {notebook_id}")
    print(f"Fetch results at {_fetch_url}")
    print("Fabric-testing submit ran successfully!")
    return _fetch_url


def main():
    args = submit_args()
    submit(args)


if __name__ == "__main__":
    main()
