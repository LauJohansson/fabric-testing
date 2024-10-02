"""
Test Plan:
Test 1: Successful notebook run:
Simulate a successful API call where the response contains
the required headers (Location, Retry-After) and a 202 Accepted status code.
Verify that the function returns the correct fetch_url and retry_after values.

Test 2: Failure to trigger notebook (non-202 response):
Simulate a failed API call with a non-202 status code,
which should raise an exception.

Test 3: Handle missing headers (e.g., Retry-After):
Simulate a response where the Retry-After header is missing,
and the function should use the default value (60 seconds).
"""

import unittest
from unittest.mock import MagicMock, patch

from fabrictesting.notebook.run import run_notebook


class TestRunNotebook(unittest.TestCase):
    @patch("fabrictesting.notebook.run.requests.post")
    def test_run_notebook_success(self, mock_post):
        """
        Test successful run_notebook triggering with valid headers and 202 response.
        """
        # Arrange: Mock a successful response with 202 status code and headers
        mock_response = MagicMock()
        mock_response.status_code = 202
        mock_response.headers = {
            "Location": "https://api.fabric.microsoft.com/v1/workspaces/test_workspace/items/test_item/jobs/instances/test_job_instance",
            "Retry-After": "30",
        }
        mock_post.return_value = mock_response

        # Act: Call the run_notebook function
        result = run_notebook(
            item_id="test_item",
            workspace_id="test_workspace",
            token_string="test_token",
        )

        # Assert: Ensure that the result contains the correct values
        expected_result = {
            "status_code": 202,
            "fetch_url": "https://api.fabric.microsoft.com/v1/workspaces/test_workspace/items/test_item/jobs/instances/test_job_instance",
            "retry_after": 30,
        }
        self.assertEqual(result, expected_result)
        mock_post.assert_called_once_with(
            url="https://api.fabric.microsoft.com/v1/workspaces/test_workspace/items/test_item/jobs/instances?jobType=RunNotebook",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer test_token",
            },
        )

    @patch("fabrictesting.notebook.run.requests.post")
    def test_run_notebook_failure(self, mock_post):
        """
        Test run_notebook triggering with a non-202 response code,
         which should raise an exception.
        """
        # Arrange: Mock a response with a non-202 status code
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.content = b"Internal Server Error"
        mock_post.return_value = mock_response

        # Act & Assert: Ensure the function raises an exception for non-202 status
        with self.assertRaises(Exception) as context:
            run_notebook(
                item_id="test_item",
                workspace_id="test_workspace",
                token_string="test_token",
            )

        self.assertIn("Triggering notebook failed with 500", str(context.exception))
        mock_post.assert_called_once_with(
            url="https://api.fabric.microsoft.com/v1/workspaces/test_workspace/items/test_item/jobs/instances?jobType=RunNotebook",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer test_token",
            },
        )

    @patch("fabrictesting.notebook.run.requests.post")
    def test_run_notebook_missing_retry_after_header(self, mock_post):
        """
        Test run_notebook triggering where the Retry-After header is missing,
        and the default value of 60 seconds is used.
        """
        # Arrange: Mock a successful response with no Retry-After header
        mock_response = MagicMock()
        mock_response.status_code = 202
        mock_response.headers = {
            "Location": "https://api.fabric.microsoft.com/v1/workspaces/test_workspace/items/test_item/jobs/instances/test_job_instance"
            # No Retry-After header
        }
        mock_post.return_value = mock_response

        # Act: Call the run_notebook function
        result = run_notebook(
            item_id="test_item",
            workspace_id="test_workspace",
            token_string="test_token",
        )

        # Assert: Ensure that the result contains the correct values,
        # with default retry_after
        expected_result = {
            "status_code": 202,
            "fetch_url": "https://api.fabric.microsoft.com/v1/workspaces/test_workspace/items/test_item/jobs/instances/test_job_instance",
            "retry_after": 60,  # Default value since Retry-After is missing
        }
        self.assertEqual(result, expected_result)
        mock_post.assert_called_once_with(
            url="https://api.fabric.microsoft.com/v1/workspaces/test_workspace/items/test_item/jobs/instances?jobType=RunNotebook",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer test_token",
            },
        )


if __name__ == "__main__":
    unittest.main()
