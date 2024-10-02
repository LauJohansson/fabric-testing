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
    Load the notebook-content.py file, replace placeholders,
        and return the modified content as a string.

    Args:
        lakehouse_id (str): The ID of the lakehouse to replace in the notebook.
        default_lakehouse_name (str): The default lakehouse name
                                      to replace in the notebook.
        default_lakehouse_workspace_id (str): The default lakehouse workspace ID
                                    to replace in the notebook.

    Returns:
        str: The notebook content with the placeholders replaced.


    See the notebook definition here:
    https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/notebook-definition
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
