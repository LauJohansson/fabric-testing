"""
Test Plan
Test 1: Simulate a successful job completion (status "Completed").
Test 2: Simulate a job failure (status "Failed") with a valid failure reason.
Test 3: Simulate a job still in progress (status "InProgress").
Test 4: Simulate a non-200 response (like 202),
which indicates the job is still running.
Test 5: Simulate a failure without a proper failure reason or message,
ensuring the correct exceptions are raised.
Test 6: Simulate handling unexpected status codes.
"""

import unittest
from unittest.mock import MagicMock, patch

from fabrictesting.notebook.get_notebook_status import (
    poll_notebook_run_status,
)


class TestNotebookStatus(unittest.TestCase):
    @patch("fabrictesting.notebook.get_notebook_status.requests.get")
    def test_poll_notebook_run_status_completed(self, mock_get):
        """
        Test poll_notebook_run_status for a job that completes successfully.
        """
        # Arrange: Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "Completed",
            "id": "job-id",
            "content": "Job content",
        }
        mock_response.content = b"Job content"
        mock_get.return_value = mock_response

        # Act: Call poll_notebook_run_status
        result = poll_notebook_run_status(
            fetch_url="https://api.fabric.microsoft.com/v1/workspaces/workspaceId/items/itemId/jobs/instances/jobInstanceId",
            retry_after=1,
            token_string="test_token",
        )

        # Assert: Ensure result is returned correctly
        self.assertEqual(result, {"status_code": 200, "content": b"Job content"})
        mock_get.assert_called()

    @patch("fabrictesting.notebook.get_notebook_status.requests.get")
    def test_poll_notebook_run_status_failed(self, mock_get):
        """
        Test poll_notebook_run_status for a job that fails.
        """
        # Arrange: Mock failed response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "Failed",
            "failureReason": {"message": "Job failed due to an unknown error."},
        }
        mock_response.content = b"Job content"
        mock_get.return_value = mock_response

        # Act: Call poll_notebook_run_status
        result = poll_notebook_run_status(
            fetch_url="https://api.fabric.microsoft.com/v1/workspaces/workspaceId/items/itemId/jobs/instances/jobInstanceId",
            retry_after=1,
            token_string="test_token",
        )

        # Assert: Ensure result contains failure details
        self.assertEqual(result, {"status_code": 200, "content": b"Job content"})
        mock_get.assert_called()

    @patch("fabrictesting.notebook.get_notebook_status.requests.get")
    def test_poll_notebook_run_status_in_progress(self, mock_get):
        """
        Test poll_notebook_run_status for a job
        that is in progress and eventually completes.
        """
        # Arrange: Simulate the job being "InProgress"
        # for the first two calls, and "Completed" after that
        mock_in_progress_response = MagicMock()
        mock_in_progress_response.status_code = 200
        mock_in_progress_response.json.return_value = {"status": "InProgress"}
        mock_in_progress_response.content = b"Job in progress"

        mock_completed_response = MagicMock()
        mock_completed_response.status_code = 200
        mock_completed_response.json.return_value = {"status": "Completed"}
        mock_completed_response.content = b"Job completed"

        # First two calls will return "InProgress", the third will return "Completed"
        mock_get.side_effect = [
            mock_in_progress_response,
            mock_in_progress_response,
            mock_completed_response,
        ]

        # Act: Call poll_notebook_run_status
        with patch(
            "time.sleep", return_value=None
        ):  # Patch sleep to avoid delays during the test
            result = poll_notebook_run_status(
                fetch_url="https://api.fabric.microsoft.com/v1/workspaces/workspaceId/items/itemId/jobs/instances/jobInstanceId",
                retry_after=1,
                token_string="test_token",
            )

        # Assert: Ensure the result returns the completed
        # job content after the in-progress retries
        self.assertEqual(result, {"status_code": 200, "content": b"Job completed"})
        mock_get.assert_called()

    @patch("fabrictesting.notebook.get_notebook_status.requests.get")
    def test_poll_notebook_run_status_non_successful_response(self, mock_get):
        """
        Test poll_notebook_run_status for a job that
        returns non-200 status code (e.g. 202 Accepted).
        """
        # Arrange: Mock 202 response (Job still running)
        mock_accepted_response = MagicMock()
        mock_accepted_response.status_code = 202
        mock_accepted_response.content = b"Job is still running"

        # Arrange: Followed by a mock response
        # that simulates a successful job completion
        mock_completed_response = MagicMock()
        mock_completed_response.status_code = 200
        mock_completed_response.json.return_value = {"status": "Completed"}
        mock_completed_response.content = b"Job completed"

        # First two responses return 202, and then the job completes with 200
        mock_get.side_effect = [
            mock_accepted_response,
            mock_accepted_response,
            mock_completed_response,
        ]

        # Act: Call poll_notebook_run_status
        with patch(
            "time.sleep", return_value=None
        ):  # Patch sleep to avoid delays during the test
            result = poll_notebook_run_status(
                fetch_url="https://api.fabric.microsoft.com/v1/workspaces/workspaceId/items/itemId/jobs/instances/jobInstanceId",
                retry_after=1,
                token_string="test_token",
            )

        # Assert: The result should return the completed job after retrying
        self.assertEqual(result, {"status_code": 200, "content": b"Job completed"})
        mock_get.assert_called()

    @patch("fabrictesting.notebook.get_notebook_status.requests.get")
    def test_poll_notebook_run_status_failed_no_reason(self, mock_get):
        """
        Test poll_notebook_run_status for a job that fails without a failure reason.
        """
        # Arrange: Mock failed response without failureReason
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "Failed", "failureReason": None}

        mock_response.content = b"Job content"
        mock_get.return_value = mock_response

        # Act & Assert: Ensure exception is raised for missing failure reason
        with self.assertRaises(Exception) as context:
            poll_notebook_run_status(
                fetch_url="https://api.fabric.microsoft.com/v1/workspaces/workspaceId/items/itemId/jobs/instances/jobInstanceId",
                retry_after=1,
                token_string="test_token",
            )
        self.assertIn("There was no failure reason", str(context.exception))

    @patch("fabrictesting.notebook.get_notebook_status.requests.get")
    def test_poll_notebook_run_status_unexpected_status(self, mock_get):
        """
        Test poll_notebook_run_status for an unexpected status code.
        """
        # Arrange: Mock unexpected status code response (e.g. 500 Internal Server Error)
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.content = b"Internal Server Error"
        mock_get.return_value = mock_response

        # Act: Call poll_notebook_run_status
        result = poll_notebook_run_status(
            fetch_url="https://api.fabric.microsoft.com/v1/workspaces/workspaceId/items/itemId/jobs/instances/jobInstanceId",
            retry_after=1,
            token_string="test_token",
        )

        # Assert: Ensure result contains error details
        self.assertEqual(
            result, {"status_code": 500, "content": b"Internal Server Error"}
        )
        mock_get.assert_called()
