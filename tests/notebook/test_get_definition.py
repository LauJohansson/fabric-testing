import json
import unittest
from unittest.mock import MagicMock, patch

from fabrictesting.notebook.get_definitions import get_notebook_id, list_notebooks


class TestNotebookDefinitions(unittest.TestCase):
    @patch("fabrictesting.notebook.get_definitions.requests.get")
    def test_list_notebooks_success(self, mock_get):
        """
        Test list_notebooks when the API returns a valid response with notebooks.
        """
        # Arrange: Define the mock response with a successful 200 status code
        mock_response_data = {
            "value": [
                {
                    "id": "3546052c-ae64-4526-b1a8-52af7761426f",
                    "displayName": "Notebook Name 1",
                }
            ]
        }
        mock_response = MagicMock()
        mock_response.content = json.dumps(mock_response_data).encode("utf-8")
        mock_response.status_code = (
            200  # Ensure it's a 200 status code (successful response)
        )
        mock_get.return_value = mock_response

        # Act: Call the list_notebooks function
        result = list_notebooks(workspace_id="workspace_123", token_string="test_token")

        # Assert: Check if the notebooks were retrieved correctly
        expected_result = {"Notebook Name 1": "3546052c-ae64-4526-b1a8-52af7761426f"}
        self.assertEqual(result, expected_result)

        # Check if the request was made to the correct URL with correct headers
        mock_get.assert_called_once_with(
            url="https://api.fabric.microsoft.com/v1/workspaces/workspace_123/notebooks",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer test_token",
            },
        )

    @patch("fabrictesting.notebook.get_definitions.requests.get")
    def test_list_notebooks_empty(self, mock_get):
        """
        Test list_notebooks when the API returns no notebooks.
        """
        # Arrange: Define the mock response
        # with an empty notebook list and a 200 status code
        mock_response_data = {"value": []}
        mock_response = MagicMock()
        mock_response.content = json.dumps(mock_response_data).encode("utf-8")
        mock_response.status_code = (
            200  # Ensure it's a 200 status code (successful response)
        )
        mock_get.return_value = mock_response

        # Act: Call the list_notebooks function
        result = list_notebooks(workspace_id="workspace_123", token_string="test_token")

        # Assert: Check if the result is an empty dictionary
        self.assertEqual(result, {})

        # Check if the request was made to the correct URL with correct headers
        mock_get.assert_called_once_with(
            url="https://api.fabric.microsoft.com/v1/workspaces/workspace_123/notebooks",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer test_token",
            },
        )

    @patch("fabrictesting.notebook.get_definitions.requests.get")
    def test_list_notebooks_api_error(self, mock_get):
        """
        Test list_notebooks when the API returns an error response.
        """
        # Arrange: Define a mock error response from the API
        mock_response = MagicMock()
        mock_response.content = json.dumps(
            {"errorCode": "401", "message": "Unauthorized"}
        ).encode("utf-8")
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        # Act & Assert: The list_notebooks function should handle the error gracefully
        with self.assertRaises(Exception) as context:
            list_notebooks(workspace_id="workspace_123", token_string="invalid_token")

        self.assertIn("Unauthorized", str(context.exception))

    @patch("fabrictesting.notebook.get_definitions.list_notebooks")
    def test_get_notebook_id_success(self, mock_list_notebooks):
        """
        Test get_notebook_id when the notebook is found.
        """
        # Arrange: Mock the list_notebooks function
        # to return a valid notebook dictionary
        mock_list_notebooks.return_value = {
            "Notebook Name 1": "3546052c-ae64-4526-b1a8-52af7761426f"
        }

        # Act: Call the get_notebook_id function
        result = get_notebook_id(
            notebook_name="Notebook Name 1",
            workspace_id="workspace_123",
            token_string="test_token",
        )

        # Assert: Check if the correct notebook ID is returned
        self.assertEqual(result, "3546052c-ae64-4526-b1a8-52af7761426f")

    @patch("fabrictesting.notebook.get_definitions.list_notebooks")
    def test_get_notebook_id_not_found(self, mock_list_notebooks):
        """
        Test get_notebook_id when the notebook is not found.
        """
        # Arrange: Mock the list_notebooks function to return an empty dictionary
        mock_list_notebooks.return_value = {}

        # Act & Assert: The get_notebook_id function
        # should raise an exception when the notebook is not found
        with self.assertRaises(Exception) as context:
            get_notebook_id(
                notebook_name="Unknown Notebook",
                workspace_id="workspace_123",
                token_string="test_token",
            )

        self.assertIn("not found", str(context.exception))
