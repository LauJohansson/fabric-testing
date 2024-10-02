import os
import unittest
from unittest.mock import mock_open, patch

from fabrictesting.notebook.create import load_default_notebook


class TestLoadDefaultNotebook(unittest.TestCase):
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="""
        # Notebook content with placeholders
        XXLAKEHOUSEIDXX
        XXDEFAULTLAKEHOUSENAMEXX
        XXDEFAULTLAKEHOUSEWORKSPACEIDXX
        XXWORKSPACENAMEXX
        XXSUBMITFOLDERXX
        XXREQUIREMENTSFILENAMEXX
        XXWHEELNAMEXX
        XXTESTFOLDERXX
    """,
    )
    @patch("os.path.dirname", return_value="/path/to/notebook")
    def test_load_default_notebook(self, mock_dirname, mock_file):
        # Arrange: Define test inputs
        lakehouse_id = "123456"
        default_lakehouse_name = "MyLakehouse"
        default_lakehouse_workspace_id = "abcdef12345"
        workspace_name = "myworkspace"
        submit_folder = "test_submission"
        requirements_file_name = "requirements.txt"
        wheel_name = "customwheel-1.0-py3-none-any.whl"
        unittest_folder_name = "unittests"

        # Act: Call the function
        result = load_default_notebook(
            lakehouse_id=lakehouse_id,
            default_lakehouse_name=default_lakehouse_name,
            default_lakehouse_workspace_id=default_lakehouse_workspace_id,
            workspace_name=workspace_name,
            submit_folder=submit_folder,
            requirements_file_name=requirements_file_name,
            wheel_name=wheel_name,
            unittest_folder_name=unittest_folder_name,
        )

        # Assert: Check that placeholders were correctly replaced
        self.assertIn(lakehouse_id, result)
        self.assertIn(default_lakehouse_name, result)
        self.assertIn(default_lakehouse_workspace_id, result)
        self.assertIn(workspace_name, result)
        self.assertIn(submit_folder, result)
        self.assertIn(requirements_file_name, result)
        self.assertIn(wheel_name, result)
        self.assertIn(unittest_folder_name, result)

        # Correct path formatting for platform
        notebook_file_path = os.path.join("/path/to/notebook", "notebook-content.py")

        # Assert the correct file was opened
        mock_file.assert_called_once_with(notebook_file_path, "r")


if __name__ == "__main__":
    unittest.main()
