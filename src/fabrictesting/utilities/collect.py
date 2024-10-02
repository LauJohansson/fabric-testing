import shutil
import tempfile
from pathlib import Path
from typing import Tuple


def create_temp_folder_with_files(
    *, tests_path: str, whl_path: str = None, requirements_file: str = None
) -> Tuple[str, str, str]:
    """
    Creates a temporary folder, renames the files as needed, and copies the
    specified wheel file, test folder, and requirements file into it.

    The files will be saved as:
        - custom.whl for the wheel file
        - tests/ for the test folder
        - requirements.txt for the requirements file

    Args:
        whl_path (str): The path to the wheel file (.whl) to copy.
        tests_path (str): The path to the directory containing unit tests.
        requirements_file (str): The path to the requirements.txt file to copy.

    Returns:
        str: The path to the created temporary directory.
    """
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Define the destination of tests
        temp_tests_dir = Path(temp_dir) / "tests"

        # Copy and rename the tests folder to 'tests'
        shutil.copytree(tests_path, temp_tests_dir)

        if whl_path:
            # Define the destination of whl
            temp_whl_path = Path(temp_dir) / Path(whl_path).name
            # Copy and rename the wheel file to 'custom.whl'
            shutil.copy2(whl_path, temp_whl_path)
            _whl_name = Path(whl_path).name
        else:
            _whl_name = None

        if requirements_file:
            # Define the destination of reqs
            temp_requirements_file = (
                Path(temp_dir) / Path(requirements_file).name
            )  # "requirements.txt"
            # Copy and rename the requirements file to 'requirements.txt'
            shutil.copy2(requirements_file, temp_requirements_file)
            _rqs_name = Path(requirements_file).name
        else:
            _rqs_name = None

        print(f"Temporary folder created at: {temp_dir}")
        return temp_dir, _whl_name, _rqs_name

    except Exception as e:  # noqa: BLE001
        # Clean up the temp folder in case of failure
        shutil.rmtree(temp_dir)
        raise RuntimeError(f"Failed to create temporary folder: {str(e)}")
