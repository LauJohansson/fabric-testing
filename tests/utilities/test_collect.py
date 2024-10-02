import unittest
from pathlib import Path
from unittest.mock import patch

from fabrictesting.utilities.collect import create_temp_folder_with_files


class TestCreateTempFolderWithFiles(unittest.TestCase):
    """
        Test Plan:
    Test with all arguments (wheel file, test folder, and requirements file):

    1: Mock all file system operations to simulate copying
    the files without actually doing it.
    Ensure that the function returns the expected paths.
    Test without optional arguments (wheel file or requirements file):

    2: Test the case where either the wheel file or the
    requirements file is not provided.
    Test failure handling:

    3: Simulate an exception during the copy operation and
    ensure the temporary directory is cleaned up.
    """

    @patch("fabrictesting.utilities.collect.shutil.rmtree")  # Mock rmtree for cleanup
    @patch("fabrictesting.utilities.collect.shutil.copy2")  # Mock copy2 for file copy
    @patch(
        "fabrictesting.utilities.collect.shutil.copytree"
    )  # Mock copytree for test folder copy
    @patch(
        "fabrictesting.utilities.collect.tempfile.mkdtemp"
    )  # Mock mkdtemp to return a dummy temp dir
    @patch("builtins.print")  # Mock print to suppress output
    def test_create_temp_folder_with_all_files(
        self, mock_print, mock_mkdtemp, mock_copytree, mock_copy2, mock_rmtree
    ):
        """
        Test create_temp_folder_with_files with all
        arguments (whl_path, tests_path, requirements_file).
        """
        # Arrange: Mock mkdtemp to return a fake temp directory path
        mock_mkdtemp.return_value = "/mock/temp/dir"

        # Act: Call the function with all arguments
        temp_dir, whl_name, rqs_name = create_temp_folder_with_files(
            tests_path="/mock/tests/path",
            whl_path="/mock/wheel/file.whl",
            requirements_file="/mock/requirements.txt",
        )

        # Assert: Ensure the expected values are returned
        self.assertEqual(temp_dir, "/mock/temp/dir")
        self.assertEqual(whl_name, "file.whl")
        self.assertEqual(rqs_name, "requirements.txt")

        # Assert that the necessary file operations were called
        mock_mkdtemp.assert_called_once()
        mock_copytree.assert_called_once_with(
            "/mock/tests/path", Path("/mock/temp/dir/tests")
        )
        mock_copy2.assert_any_call(
            "/mock/wheel/file.whl", Path("/mock/temp/dir/file.whl")
        )
        mock_copy2.assert_any_call(
            "/mock/requirements.txt", Path("/mock/temp/dir/requirements.txt")
        )
        mock_print.assert_called_once_with(
            "Temporary folder created at: /mock/temp/dir"
        )

    @patch("fabrictesting.utilities.collect.shutil.rmtree")  # Mock rmtree for cleanup
    @patch("fabrictesting.utilities.collect.shutil.copy2")  # Mock copy2 for file copy
    @patch(
        "fabrictesting.utilities.collect.shutil.copytree"
    )  # Mock copytree for test folder copy
    @patch(
        "fabrictesting.utilities.collect.tempfile.mkdtemp"
    )  # Mock mkdtemp to return a dummy temp dir
    @patch("builtins.print")  # Mock print to suppress output
    def test_create_temp_folder_without_optional_files(
        self, mock_print, mock_mkdtemp, mock_copytree, mock_copy2, mock_rmtree
    ):
        """
        Test create_temp_folder_with_files without optional
         arguments (no whl_path, no requirements_file).
        """
        # Arrange: Mock mkdtemp to return a fake temp directory path
        mock_mkdtemp.return_value = "/mock/temp/dir"

        # Act: Call the function without whl_path and requirements_file
        temp_dir, whl_name, rqs_name = create_temp_folder_with_files(
            tests_path="/mock/tests/path", whl_path=None, requirements_file=None
        )

        # Assert: Ensure the expected values are returned
        self.assertEqual(temp_dir, "/mock/temp/dir")
        self.assertIsNone(whl_name)
        self.assertIsNone(rqs_name)

        # Assert that only the necessary file operations were called
        mock_mkdtemp.assert_called_once()
        mock_copytree.assert_called_once_with(
            "/mock/tests/path", Path("/mock/temp/dir/tests")
        )
        # copy2 should not be called since there's no whl or requirements
        mock_copy2.assert_not_called()
        mock_print.assert_called_once_with(
            "Temporary folder created at: /mock/temp/dir"
        )

    @patch("fabrictesting.utilities.collect.shutil.rmtree")  # Mock rmtree for cleanup
    @patch(
        "fabrictesting.utilities.collect.shutil.copytree"
    )  # Mock copytree for test folder copy
    @patch(
        "fabrictesting.utilities.collect.tempfile.mkdtemp"
    )  # Mock mkdtemp to return a dummy temp dir
    def test_create_temp_folder_failure(self, mock_mkdtemp, mock_copytree, mock_rmtree):
        """
        Test create_temp_folder_with_files raises RuntimeError
        on failure and cleans up the temp folder.
        """
        # Arrange: Mock mkdtemp to return a fake temp directory path
        mock_mkdtemp.return_value = "/mock/temp/dir"

        # Simulate an exception during copytree
        mock_copytree.side_effect = Exception("Copy failed")

        # Act & Assert: Ensure that RuntimeError is raised and cleanup is performed
        with self.assertRaises(RuntimeError) as context:
            create_temp_folder_with_files(
                tests_path="/mock/tests/path",
                whl_path="/mock/wheel/file.whl",
                requirements_file="/mock/requirements.txt",
            )

        # Assert: Ensure that rmtree is called to clean up the temp directory
        mock_rmtree.assert_called_once_with("/mock/temp/dir")
        self.assertIn(
            "Failed to create temporary folder: Copy failed", str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
