import unittest
from unittest.mock import MagicMock, call, patch

from fabrictesting.notebook.upload import upload_notebook


class TestUploadNotebook(unittest.TestCase):
    """
    Test Plan:
    Test successful notebook creation (201 status):

    1: Simulate a response where the notebook is successfully created with status 201.
    Test notebook creation in progress (202 status):

    2: Simulate a response with status 202 where notebook provisioning is in progress.
    Mock poll_notebook_upload_status to simulate polling for the notebook status.
    Test failure during notebook upload (non-201/202 status):

    3: Simulate a response with a status code
    other than 201 or 202 to trigger an exception.


    """

    @patch("fabrictesting.notebook.upload.poll_notebook_upload_status")
    @patch("fabrictesting.notebook.upload.requests.post")
    @patch("fabrictesting.notebook.upload.convert_notebook_into_inlinebase64")
    @patch("fabrictesting.notebook.upload.convert_platform_into_inlinebase64")
    @patch("builtins.print")  # Mock the print function
    def test_upload_notebook_success(
        self,
        mock_print,
        mock_convert_platform,
        mock_convert_notebook,
        mock_post,
        mock_poll,
    ):
        """
        Test upload_notebook when the notebook
        is successfully created (201 status code).
        """
        # Arrange: Mock the payload conversion functions
        mock_convert_notebook.return_value = "mock_notebook_base64"
        mock_convert_platform.return_value = "mock_platform_base64"

        # Arrange: Mock a successful response from the post request
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        # Act: Call the upload_notebook function
        result = upload_notebook(
            display_name="Test Notebook",
            description="Test Description",
            notebook_definition="mock_notebook_content",
            platform_definition="mock_platform_content",
            workspace_id="mock_workspace_id",
            token_string="mock_token",
        )

        # Assert: Ensure that the response returns the correct values
        self.assertEqual(result["status_code"], 201)
        mock_post.assert_called_once()

        # Assert that the correct print statements were called
        expected_print_calls = [
            call("Prepare uploading notebook..."),
            call("    Display Name: Test Notebook"),
            call("    To workspace with id: mock_workspace_id"),
            call("Converting notebook payload to base64..."),
            call("Converting platform payload to base64..."),
            call("Posting notebook..."),
            call("Posting finished!"),
            call("Notebook was successfully created!"),
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)

    @patch("fabrictesting.notebook.upload.poll_notebook_upload_status")
    @patch("fabrictesting.notebook.upload.requests.post")
    @patch("fabrictesting.notebook.upload.convert_notebook_into_inlinebase64")
    @patch("fabrictesting.notebook.upload.convert_platform_into_inlinebase64")
    @patch("builtins.print")  # Mock the print function
    def test_upload_notebook_in_progress(
        self,
        mock_print,
        mock_convert_platform,
        mock_convert_notebook,
        mock_post,
        mock_poll,
    ):
        """
        Test upload_notebook when the notebook is in progress (202 status code).
        """
        # Arrange: Mock the payload conversion functions
        mock_convert_notebook.return_value = "mock_notebook_base64"
        mock_convert_platform.return_value = "mock_platform_base64"

        # Arrange: Mock a 202 response from the post request and a poll response
        mock_response = MagicMock()
        mock_response.status_code = 202
        mock_response.headers = {"Location": "mock_location_url", "Retry-After": "10"}
        mock_post.return_value = mock_response

        # Mock the polling response
        mock_poll_response = MagicMock()
        mock_poll_response.status_code = 200
        mock_poll_response.content = b"Notebook polling completed"
        mock_poll.return_value = mock_poll_response

        # Act: Call the upload_notebook function
        result = upload_notebook(
            display_name="Test Notebook",
            description="Test Description",
            notebook_definition="mock_notebook_content",
            platform_definition="mock_platform_content",
            workspace_id="mock_workspace_id",
            token_string="mock_token",
        )

        # Assert: Ensure that the polling was called and the response is correct
        self.assertEqual(result["status_code"], 200)
        self.assertEqual(result["content"], b"Notebook polling completed")
        mock_post.assert_called_once()
        mock_poll.assert_called_once_with("mock_location_url", 10, "mock_token")

        # Assert that the correct print statements were called
        expected_print_calls = [
            call("Prepare uploading notebook..."),
            call("    Display Name: Test Notebook"),
            call("    To workspace with id: mock_workspace_id"),
            call("Converting notebook payload to base64..."),
            call("Converting platform payload to base64..."),
            call("Posting notebook..."),
            call("Posting finished!"),
            call("Notebook Request accepted, notebook provisioning in progress..."),
            call("To check the status, polling the following URL: mock_location_url"),
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)

    @patch("fabrictesting.notebook.upload.requests.post")
    @patch("fabrictesting.notebook.upload.convert_notebook_into_inlinebase64")
    @patch("fabrictesting.notebook.upload.convert_platform_into_inlinebase64")
    @patch("builtins.print")  # Mock the print function
    def test_upload_notebook_failure(
        self, mock_print, mock_convert_platform, mock_convert_notebook, mock_post
    ):
        """
        Test upload_notebook when the notebook
         upload fails with a non-201/202 status code.
        """
        # Arrange: Mock the payload conversion functions
        mock_convert_notebook.return_value = "mock_notebook_base64"
        mock_convert_platform.return_value = "mock_platform_base64"

        # Arrange: Mock a failed response from the post request
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.content = b"Internal Server Error"
        mock_post.return_value = mock_response

        # Act & Assert: Ensure that an exception is raised for the failed upload
        with self.assertRaises(Exception) as context:
            upload_notebook(
                display_name="Test Notebook",
                description="Test Description",
                notebook_definition="mock_notebook_content",
                platform_definition="mock_platform_content",
                workspace_id="mock_workspace_id",
                token_string="mock_token",
            )

        self.assertIn(
            "Notebook upload failed with status code 500", str(context.exception)
        )
        mock_post.assert_called_once()

        # Assert that the correct print statements were called
        expected_print_calls = [
            call("Prepare uploading notebook..."),
            call("    Display Name: Test Notebook"),
            call("    To workspace with id: mock_workspace_id"),
            call("Converting notebook payload to base64..."),
            call("Converting platform payload to base64..."),
            call("Posting notebook..."),
            call("Posting finished!"),
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)
