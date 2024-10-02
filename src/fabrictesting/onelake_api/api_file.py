import os
import uuid
from datetime import datetime

from azure.storage.filedatalake import FileSystemClient

from fabrictesting.onelake_api.api_access import get_service_client


def upload_folder_to_onelake(
    *,
    temp_folder: str,
    workspace_name: str,
    lakehouse_name: str,
    custom_folder: str = None,
) -> str:
    """
    Uploads the contents of the temporary folder to
    OneLake DataLake.

    The target directory is defined as:
        - 'fabric-testing'
        - _uuid: A generated UUID
        - _timestamp: Current timestamp in 'ddmmyyyy-hhmm' format
        - _test_folder: Combined _timestamp and _uuid


    Args:
        temp_folder (str): The path to the local folder containing the files to upload.
        workspace_name (str): The name of the file system (equivalent to a container).
        lakehouse_name (str): The name of the lakehouse.
        custom_folder (str, optional): A custom folder name for the destination.
            If not provided, a folder name is generated using a UUID and timestamp.

    Raises:
        RuntimeError: If any file upload fails.

    :return
        test_folder: Name of the test folder
    """
    try:
        # Generate UUID and timestamp
        if custom_folder:
            _test_folder = custom_folder
        else:
            # Shorten UUID to first 8 characters
            _uuid = uuid.uuid4().hex[:8]
            # Timestamp format: ddmmyyyy-hhmm
            _timestamp = datetime.now().strftime("%d%m%Y-%H%M")
            # Combine timestamp and UUID to form test folder name
            _test_folder = f"fabric-testing-{_timestamp}_{_uuid}"

        # Define the target directory path based on lakehouse_name
        target_directory = (
            f"{lakehouse_name}.Lakehouse/Files/fabric-testing/{_test_folder}"
        )

        print(
            f"Authenticating and getting the service "
            f"client for workspace: {workspace_name}"
        )
        # Step 1: Authenticate and get service
        # client using the provided token
        service_client = get_service_client()

        print(f"Creating FileSystemClient for workspace: {workspace_name}")
        # Step 2: Create FileSystemClient for the desired file system (workspace)
        file_system_client = service_client.get_file_system_client(
            file_system=workspace_name
        )

        print(
            f"Starting to upload files from folder: {temp_folder} to {target_directory}"
        )
        print("=" * 50)
        # Step 3: Upload files from the temp folder to OneLake
        for root, _, files in os.walk(temp_folder):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, temp_folder)
                upload_path = f"{target_directory}/{relative_path}"

                # Upload each file
                upload_file_to_onelake(file_system_client, upload_path, file_path)
        print("=" * 50)
        print(
            f"Successfully uploaded folder to "
            f"{lakehouse_name}.Lakehouse/Files/fabric-testing/{_test_folder}"
        )

        return _test_folder
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"Failed to upload folder: {str(e)}")


def upload_file_to_onelake(
    file_system_client: FileSystemClient, destination_path: str, local_file_path: str
):
    """
    Uploads a single file to OneLake's DataLake.

    This function uploads a specific file from a local directory
    to a designated path in OneLake. It creates a DataLake file client
    and handles the file upload to the OneLake storage.

    Args:
        file_system_client (FileSystemClient):
            The client for interacting with the OneLake file system.
        destination_path (str):
            The target path in OneLake where the file will be uploaded.
        local_file_path (str):
            The path to the local file to be uploaded.

    Raises:
        RuntimeError: If the file upload fails due to any exception.
    """

    try:
        print(f"Creating DataLake file client for path: {destination_path}")
        # Create a DataLake file client to interact with the destination path
        file_client = file_system_client.get_file_client(destination_path)

        print(f"Preparing {local_file_path} for {destination_path}")
        # Upload the file
        with open(local_file_path, "rb") as file_data:
            file_client.upload_data(file_data, overwrite=True)

        print(f"Uploaded {local_file_path} to {destination_path}")

    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"Failed to upload file {local_file_path}: {str(e)}")
