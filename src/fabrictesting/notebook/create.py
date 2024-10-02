import base64
import json
import os
import uuid


def load_default_notebook(
    *,
    lakehouse_id: str,
    default_lakehouse_name: str,
    default_lakehouse_workspace_id: str,
    workspace_name: str,
    submit_folder: str,
    wheel_name: str = None,
    requirements_file_name: str = None,
    unittest_folder_name: str = "tests",
) -> str:
    """
    Loads and modifies the default notebook content
    by replacing placeholder values with actual parameters.

    This function reads the content of a notebook file (in `.ipynb` format)
    and replaces certain placeholderswith the provided values for lakehouse IDs,
    workspace names, and file paths. It also manages optional
    installation of dependencies via pip by replacing or removing
    the relevant installation commands based
    on whether `wheel_name` or `requirements_file_name` is provided.

    Args:
        lakehouse_id (str):
            The identifier for the lakehouse.
        default_lakehouse_name (str):
            The default name of the lakehouse.
        default_lakehouse_workspace_id (str):
            The workspace ID associated with the default lakehouse.
        workspace_name (str):
            The name of the workspace where the notebook is submitted.
        submit_folder (str):
            The folder path where submission-related files are stored.
        wheel_name (str, optional):
            The name of the wheel file for dependency installation. If not provided,
            the pip install command for the wheel will be removed from the notebook.
            Defaults to None.
        requirements_file_name (str, optional):
            The name of the requirements file for dependency installation.
            If not provided, the pip install command for the requirements
            file will be removed from the notebook.
            Defaults to None.
        unittest_folder_name (str, optional):
            The folder name where unit tests are located. Defaults to "tests".

    Returns:
        str: The notebook content with placeholders replaced by the provided values.

    Raises:
        FileNotFoundError: If the notebook file cannot be found at the expected path.

    See Also:
        Notebook definition: https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/notebook-definition
    """

    # Get the current directory of the create.py file
    # (which should be the "notebook" folder)
    current_dir = os.path.dirname(__file__)
    # Path to the notebook-content.py file in the same folder
    notebook_file_path = os.path.join(current_dir, "notebook-content.ipynb")

    # Load the content of the notebook-content.py file
    try:
        with open(notebook_file_path, "r") as file:
            notebook_content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {notebook_file_path} could not be found.")

    if wheel_name is None:
        _whl_content_to_remove = "!pip install builtin/XXSUBMITFOLDERXX/XXWHEELNAMEXX"
        notebook_content = notebook_content.replace(_whl_content_to_remove, "#")

    else:
        notebook_content = notebook_content.replace("XXWHEELNAMEXX", wheel_name)

    if requirements_file_name is None:
        _rqs_content_to_remove = (
            "!pip install -r builtin/XXSUBMITFOLDERXX/XXREQUIREMENTSFILENAMEXX"
        )
        notebook_content = notebook_content.replace(_rqs_content_to_remove, "#")
    else:
        notebook_content = notebook_content.replace(
            "XXREQUIREMENTSFILENAMEXX", requirements_file_name
        )

    # Replace placeholders with actual values
    notebook_content = notebook_content.replace("XXLAKEHOUSEIDXX", lakehouse_id)
    notebook_content = notebook_content.replace(
        "XXDEFAULTLAKEHOUSENAMEXX", default_lakehouse_name
    )
    notebook_content = notebook_content.replace(
        "XXDEFAULTLAKEHOUSEWORKSPACEIDXX", default_lakehouse_workspace_id
    )
    notebook_content = notebook_content.replace("XXWORKSPACENAMEXX", workspace_name)
    notebook_content = notebook_content.replace("XXSUBMITFOLDERXX", submit_folder)

    notebook_content = notebook_content.replace("XXTESTFOLDERXX", unittest_folder_name)

    # Return the modified notebook content as a string
    return notebook_content


def convert_notebook_into_inlinebase64(notebook_content: str) -> str:
    """
    Converts the notebook content (string) into an inline Base64-encoded string.

    Args:
        notebook_content (str): The notebook content returned by
        the load_default_notebook function.

    Returns:
        str: Base64-encoded string of the notebook content.
    """
    # Convert the notebook content (string) to bytes
    notebook_bytes = notebook_content.encode("utf-8")

    # Encode the notebook bytes into Base64
    base64_bytes = base64.b64encode(notebook_bytes)

    # Convert Base64 bytes back to a string
    base64_string = base64_bytes.decode("utf-8")

    return base64_string


def create_platform_file_content(*, display_name: str, description: str = "") -> str:
    """
    Creates a JSON-formatted string representing platform file content with metadata
    and configuration.

    This function generates a JSON object with a schema reference,
    metadata for a notebook (including display name and description),
    and a configuration that includes a unique logical ID.
    The metadata and configuration adhere to the Microsoft Fabric platform
    properties schema.

    Args:
        display_name (str): The display name for the notebook in the platform.
        description (str, optional): A brief description of the notebook.
        Defaults to an empty string.

    Returns:
        str: A JSON-formatted string representing the platform file content,
        including metadata and a unique logical ID.



    """
    _uuid = uuid.uuid4().hex

    _content = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {
            "type": "Notebook",
            "displayName": display_name,
            "description": description,
        },
        "config": {"version": "2.0", "logicalId": _uuid},
    }

    return json.dumps(_content)


def convert_platform_into_inlinebase64(platform_content: str) -> str:
    """
    Converts the platform content (string) into an inline Base64-encoded string.

    Args:
        platform_content (str): The platform content returned
        by the create_platform_file_content function.

    Returns:
        str: Base64-encoded string of the notebook content.
    """
    # Convert the notebook content (string) to bytes
    notebook_bytes = platform_content.encode("utf-8")

    # Encode the notebook bytes into Base64
    base64_bytes = base64.b64encode(notebook_bytes)

    # Convert Base64 bytes back to a string
    base64_string = base64_bytes.decode("utf-8")

    return base64_string
