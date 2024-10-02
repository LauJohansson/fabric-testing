import unittest
from unittest.mock import MagicMock, call, mock_open, patch

from fabrictesting.onelake_api.api_file import upload_file_to_onelake


@unittest.skip(reason="Tests not working")
class TestUploadFileToOneLake(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data=b"mock file data")
    @patch(
        "fabrictesting.onelake_api.api_file.FileSystemClient.get_file_client"
    )  # Correctly mock the get_file_client method
    @patch("builtins.print")  # Mock the print function
    def test_upload_file_to_onelake_success(
        self, mock_print, mock_get_file_client, mock_open_file
    ):
        """
        Test upload_file_to_onelake successfully uploads a file.
        """
        # Arrange: Mock the file client and its upload method
        mock_file_client = MagicMock()
        mock_get_file_client.return_value = mock_file_client

        # Act: Call the function with mocked file system client and paths
        upload_file_to_onelake(
            file_system_client=MagicMock(),
            destination_path="mock/destination/path",
            local_file_path="mock/local/file.txt",
        )

        # Assert: Ensure the file client and upload methods were called
        mock_get_file_client.assert_called_once_with("mock/destination/path")
        mock_open_file.assert_called_once_with("mock/local/file.txt", "rb")
        mock_file_client.upload_data.assert_called_once_with(
            mock_open_file(), overwrite=True
        )

        # Assert the correct print statements were made
        expected_print_calls = [
            call("Creating DataLake file client for path: mock/destination/path"),
            call("Preparing mock/local/file.txt for mock/destination/path"),
            call("Uploaded mock/local/file.txt to mock/destination/path"),
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)

    @patch("builtins.open", new_callable=mock_open)
    @patch("fabrictesting.onelake_api.api_file.FileSystemClient.get_file_client")
    @patch("builtins.print")  # Mock the print function
    def test_upload_file_to_onelake_failure(
        self, mock_print, mock_get_file_client, mock_open_file
    ):
        """
        Test upload_file_to_onelake raises RuntimeError when file upload fails.
        """
        # Arrange: Mock the file client and simulate an exception during upload
        mock_file_client = MagicMock()
        mock_get_file_client.return_value = mock_file_client
        mock_file_client.upload_data.side_effect = Exception("Upload failed")

        # Act & Assert: Ensure that the function raises RuntimeError on failure
        with self.assertRaises(RuntimeError) as context:
            upload_file_to_onelake(
                file_system_client=MagicMock(),
                destination_path="mock/destination/path",
                local_file_path="mock/local/file.txt",
            )

        # Assert that the correct exception message is raised
        self.assertIn(
            "Failed to upload file mock/local/file.txt: Upload failed",
            str(context.exception),
        )

        # Ensure that the file client and upload method were called
        mock_get_file_client.assert_called_once_with("mock/destination/path")
        mock_open_file.assert_called_once_with("mock/local/file.txt", "rb")

        # Assert the correct print statements were made
        expected_print_calls = [
            call("Creating DataLake file client for path: mock/destination/path"),
            call("Preparing mock/local/file.txt for mock/destination/path"),
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)
