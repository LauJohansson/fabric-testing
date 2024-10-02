import os
import unittest
from unittest.mock import mock_open, patch

from fabrictesting.notebook.create import load_default_notebook


class TestNotebookCreate(unittest.TestCase):
    @patch("fabrictesting.notebook.create.os.path.dirname")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="XXLAKEHOUSEIDXX "
        "XXDEFAULTLAKEHOUSENAMEXX "
        "XXDEFAULTLAKEHOUSEWORKSPACEIDXX "
        "XXWORKSPACENAMEXX "
        "XXSUBMITFOLDERXX "
        "XXWHEELNAMEXX "
        "XXREQUIREMENTSFILENAMEXX XXTESTFOLDERXX",
    )
    def test_load_default_notebook_with_all_arguments(self, mock_file, mock_dirname):
        """
        Test load_default_notebook when all arguments are provided.
        """
        mock_dirname.return_value = "/mock/path"

        # Call the function with all arguments
        result = load_default_notebook(
            lakehouse_id="lakehouse_id_123",
            default_lakehouse_name="default_lakehouse_name",
            default_lakehouse_workspace_id="workspace_id_123",
            workspace_name="mock_workspace",
            submit_folder="mock_folder",
            wheel_name="mock_wheel.whl",
            requirements_file_name="requirements.txt",
            unittest_folder_name="unittest_folder",
        )

        # Create the expected path using os.path.join to make it cross-platform
        expected_path = os.path.join("/mock/path", "notebook-content.ipynb")

        # Assert the file was opened correctly
        mock_file.assert_called_once_with(expected_path, "r")

        # Assert the placeholders were correctly replaced
        expected_result = (
            "lakehouse_id_123 default_lakehouse_name workspace_id_123 mock_workspace "
            "mock_folder mock_wheel.whl requirements.txt unittest_folder"
        )
        self.assertEqual(result, expected_result)

    @patch("fabrictesting.notebook.create.os.path.dirname")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="XXLAKEHOUSEIDXX "
        "XXDEFAULTLAKEHOUSENAMEXX "
        "XXDEFAULTLAKEHOUSEWORKSPACEIDXX "
        "XXWORKSPACENAMEXX "
        "XXSUBMITFOLDERXX "
        "!pip install builtin/XXSUBMITFOLDERXX/XXWHEELNAMEXX "
        "!pip install -r "
        "builtin/XXSUBMITFOLDERXX/XXREQUIREMENTSFILENAMEXX "
        "XXTESTFOLDERXX",
    )
    def test_load_default_notebook_with_missing_wheel_and_requirements(
        self, mock_file, mock_dirname
    ):
        """
        Test load_default_notebook when wheel_name and requirements_file_name are None.
        """
        mock_dirname.return_value = "/mock/path"

        # Call the function without wheel_name and requirements_file_name
        result = load_default_notebook(
            lakehouse_id="lakehouse_id_123",
            default_lakehouse_name="default_lakehouse_name",
            default_lakehouse_workspace_id="workspace_id_123",
            workspace_name="mock_workspace",
            submit_folder="mock_folder",
            wheel_name=None,
            requirements_file_name=None,
            unittest_folder_name="unittest_folder",
        )

        # Create the expected path using os.path.join to make it cross-platform
        expected_path = os.path.join("/mock/path", "notebook-content.ipynb")

        # Assert the file was opened correctly
        mock_file.assert_called_once_with(expected_path, "r")

        # Assert that the wheel and requirements commands were commented out
        expected_result = (
            "lakehouse_id_123 default_lakehouse_name workspace_id_123 mock_workspace "
            "mock_folder # # unittest_folder"
        )
        self.assertEqual(result, expected_result)

    @patch("fabrictesting.notebook.create.os.path.dirname")
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_load_default_notebook_file_not_found(self, mock_file, mock_dirname):
        """
        Test load_default_notebook raises FileNotFoundError when the file is missing.
        """
        mock_dirname.return_value = "/mock/path"
        mock_file.side_effect = FileNotFoundError

        with self.assertRaises(FileNotFoundError):
            load_default_notebook(
                lakehouse_id="lakehouse_id_123",
                default_lakehouse_name="default_lakehouse_name",
                default_lakehouse_workspace_id="workspace_id_123",
                workspace_name="mock_workspace",
                submit_folder="mock_folder",
            )


if __name__ == "__main__":
    unittest.main()
