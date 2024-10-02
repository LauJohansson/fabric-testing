import unittest
from unittest.mock import mock_open, patch

from fabrictesting.notebook.create import load_default_notebook


class TestLoadDefaultNotebook(unittest.TestCase):
    # Helper function to read expected output
    def read_expected_output(self, filename):
        with open(filename, "r") as file:
            return file.read()

    @patch("fabrictesting.notebook.create.os.path.dirname")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_default_notebook_standard(self, mock_file, mock_dirname):
        """
        Test load_default_notebook with all arguments (standard case).
        """
        # Mock reading the standard notebook content
        mock_file.return_value.read.return_value = self.read_expected_output(
            "dummy_notebook/notebook-content-standard.ipynb"
        )
        mock_dirname.return_value = "/mock/path"

        # Call the function
        result = load_default_notebook(
            lakehouse_id="test_default_lakehouse_id",
            default_lakehouse_name="test_default_lakehouse_name",
            default_lakehouse_workspace_id="test_default_lakehouse_workspace_id",
            workspace_name="test_workspace",
            submit_folder="mock_folder",
            wheel_name="mock_wheel.whl",
            requirements_file_name="requirements.txt",
        )

        # Load expected output for comparison
        expected_output = self.read_expected_output(
            "dummy_notebook/expected/notebook-content-standard.ipynb"
        )

        # Compare the output with the expected content
        self.assertEqual(result, expected_output)

    @patch("fabrictesting.notebook.create.os.path.dirname")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_default_notebook_no_requirements(self, mock_file, mock_dirname):
        """
        Test load_default_notebook without requirements file.
        """
        # Mock reading the notebook content
        mock_file.return_value.read.return_value = self.read_expected_output(
            "dummy_notebook/notebook-content-standard-no-reqs.ipynb"
        )
        mock_dirname.return_value = "/mock/path"

        # Call the function without requirements file
        result = load_default_notebook(
            lakehouse_id="test_default_lakehouse_id",
            default_lakehouse_name="test_default_lakehouse_name",
            default_lakehouse_workspace_id="test_default_lakehouse_workspace_id",
            workspace_name="test_workspace",
            submit_folder="mock_folder",
            wheel_name="mock_wheel.whl",
            requirements_file_name=None,
        )

        # Load expected output for comparison
        expected_output = self.read_expected_output(
            "dummy_notebook/expected/notebook-content-standard-no-reqs.ipynb"
        )

        # Compare the output with the expected content
        self.assertEqual(result, expected_output)

    @patch("fabrictesting.notebook.create.os.path.dirname")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_default_notebook_no_requirements_no_wheel(
        self, mock_file, mock_dirname
    ):
        """
        Test load_default_notebook without requirements file and wheel file.
        """
        # Mock reading the notebook content
        mock_file.return_value.read.return_value = self.read_expected_output(
            "dummy_notebook/notebook-content-standard-no-reqs-no-wheel.ipynb"
        )
        mock_dirname.return_value = "/mock/path"

        # Call the function without requirements and wheel files
        result = load_default_notebook(
            lakehouse_id="test_default_lakehouse_id",
            default_lakehouse_name="test_default_lakehouse_name",
            default_lakehouse_workspace_id="test_default_lakehouse_workspace_id",
            workspace_name="test_workspace",
            submit_folder="mock_folder",
            wheel_name=None,
            requirements_file_name=None,
        )

        # Load expected output for comparison
        expected_output = self.read_expected_output(
            "dummy_notebook/expected/notebook-content-standard-no-reqs-no-wheel.ipynb"
        )

        # Compare the output with the expected content
        self.assertEqual(result, expected_output)

    @patch("fabrictesting.notebook.create.os.path.dirname")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_default_notebook_no_wheel(self, mock_file, mock_dirname):
        """
        Test load_default_notebook without wheel file.
        """
        # Mock reading the notebook content
        mock_file.return_value.read.return_value = self.read_expected_output(
            "dummy_notebook/notebook-content-standard-no-wheel.ipynb"
        )
        mock_dirname.return_value = "/mock/path"

        # Call the function without wheel file
        result = load_default_notebook(
            lakehouse_id="test_default_lakehouse_id",
            default_lakehouse_name="test_default_lakehouse_name",
            default_lakehouse_workspace_id="test_default_lakehouse_workspace_id",
            workspace_name="test_workspace",
            submit_folder="mock_folder",
            wheel_name=None,
            requirements_file_name="requirements.txt",
        )

        # Load expected output for comparison
        expected_output = self.read_expected_output(
            "dummy_notebook/expected/notebook-content-standard-no-wheel.ipynb"
        )

        # Compare the output with the expected content
        self.assertEqual(result, expected_output)
