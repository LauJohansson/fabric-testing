import json
import unittest
from unittest.mock import MagicMock, call, patch

from fabrictesting.notebook.upload import poll_notebook_upload_status


class TestPollNotebookUploadStatus(unittest.TestCase):
    """
    Test Plan:
    Test 1: Simulate a response where the notebook creation progress is below 100%,
    and the function retries after the specified time.
    Test 2: Simulate a successful response where the notebook
    creation progress reaches 100%.
    Test 3: Simulate a response with an unexpected status code to ensure
    the loop breaks and the function terminates.

    """

    class TestPollNotebookUploadStatus(unittest.TestCase):
        @patch("fabrictesting.notebook.upload.requests.get")
        @patch("time.sleep", return_value=None)  # To avoid real sleep during tests
        @patch("builtins.print")  # Mock the print function
        def test_poll_notebook_upload_in_progress(
            self, mock_print, mock_sleep, mock_get
        ):
            """
            Test poll_notebook_upload_status where the notebook
            creation progress is less than 100%.
            It should retry after the specified time and then simulate completion.
            """
            # Arrange: Mock in-progress response (percentComplete < 100)
            mock_in_progress_response = MagicMock()
            mock_in_progress_response.status_code = 202
            mock_in_progress_response.content = json.dumps(
                {"percentComplete": 50}
            ).encode("utf-8")

            # Arrange: Mock completed response (percentComplete = 100)
            mock_completed_response = MagicMock()
            mock_completed_response.status_code = 200
            mock_completed_response.content = json.dumps(
                {"percentComplete": 100}
            ).encode("utf-8")

            # First two calls will return "in-progress",
            # third call will return "completed"
            mock_get.side_effect = [
                mock_in_progress_response,
                mock_in_progress_response,
                mock_completed_response,
            ]

            # Act: Call the function with polling
            result = poll_notebook_upload_status(
                location_url="https://api.fabric.microsoft.com/v1/notebooks/status",
                retry_after=5,
                token_string="test_token",
            )

            # Assert: Ensure that the function
            # returns the completed result after retries
            self.assertEqual(result.status_code, 200)
            self.assertEqual(json.loads(result.content), {"percentComplete": 100})

            # Ensure requests.get was called 3 times (2 retries and then success)
            self.assertEqual(mock_get.call_count, 3)
            mock_sleep.assert_called_with(5)

            # Assert: Check that the expected print outputs were called
            expected_print_calls = [
                call("Notebook creation is at 50/100 %..."),
                call("Retrying after 5 seconds..."),
                call("Notebook creation is at 50/100 %..."),
                call("Retrying after 5 seconds..."),
                call("Notebook creation is at 100/100 %!"),
                call("Notebook creation completed."),
            ]
            mock_print.assert_has_calls(expected_print_calls, any_order=False)

    @patch("fabrictesting.notebook.upload.requests.get")
    @patch("time.sleep", return_value=None)  # To avoid real sleep during tests
    @patch("builtins.print")  # Mock the print function
    def test_poll_notebook_upload_completed(self, mock_print, mock_sleep, mock_get):
        """
        Test poll_notebook_upload_status where the notebook creation is completed.
        It should return the response once the progress reaches 100%.
        """
        # Arrange: Mock response for completed notebook (percentComplete = 100)
        mock_completed_response = MagicMock()
        mock_completed_response.status_code = 200
        mock_completed_response.content = json.dumps({"percentComplete": 100}).encode(
            "utf-8"
        )

        # Act: Call the function with the completed response
        mock_get.return_value = mock_completed_response
        result = poll_notebook_upload_status(
            location_url="https://api.fabric.microsoft.com/v1/notebooks/status",
            retry_after=5,
            token_string="test_token",
        )

        # Assert: Ensure that the function returns the response after completion
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.content), {"percentComplete": 100})
        mock_get.assert_called_once()

        # Assert that the correct print statements were called
        expected_print_calls = [
            call("Notebook creation is at 100/100 %!"),
            call("Notebook creation completed."),
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)

    @patch("fabrictesting.notebook.upload.requests.get")
    @patch("time.sleep", return_value=None)  # To avoid real sleep during tests
    @patch("builtins.print")  # Mock the print function
    def test_poll_notebook_upload_unexpected_status_code(
        self, mock_print, mock_sleep, mock_get
    ):
        """
        Test poll_notebook_upload_status where an unexpected status code is returned.
        It should break the loop and stop retrying, and print an appropriate message.
        """
        # Arrange: Mock an unexpected status code response
        mock_unexpected_response = MagicMock()
        mock_unexpected_response.status_code = 500
        mock_unexpected_response.content = b"Internal Server Error"

        # Act: Call the function with the unexpected response
        mock_get.return_value = mock_unexpected_response
        result = poll_notebook_upload_status(
            location_url="https://api.fabric.microsoft.com/v1/notebooks/status",
            retry_after=5,
            token_string="test_token",
        )

        # Assert: Ensure that the function breaks out
        # and returns the response with the unexpected status code and content
        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.content, b"Internal Server Error")
        mock_get.assert_called_once()

        # Assert that the print statement was called for the JSONDecodeError handling
        mock_print.assert_has_calls(
            [call("Unexpected status code: 500, details: b'Internal Server Error'")]
        )
