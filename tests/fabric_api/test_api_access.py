import unittest
from unittest.mock import MagicMock, patch

from fabrictesting.fabric_api.api_access import (
    get_client_fabric_token,
    get_personal_fabric_token,
)


class TestFabricApiAccess(unittest.TestCase):
    @patch("fabrictesting.fabric_api.api_access.InteractiveBrowserCredential")
    def test_get_personal_fabric_token_success(self, mock_interactive_credential):
        """
        Test the get_personal_fabric_token function when a valid token is returned.
        """
        # Mocking the token
        mock_token = MagicMock()
        mock_token.token = "mock_token_string"

        # Mocking the InteractiveBrowserCredential to return a mocked token
        mock_instance = mock_interactive_credential.return_value
        mock_instance.get_token.return_value = mock_token

        # Call the function and assert the result
        token = get_personal_fabric_token("mock_tenant_id")
        self.assertEqual(token, "mock_token_string")

        # Assert that get_token was called with the correct scope
        mock_instance.get_token.assert_called_once_with(
            "https://api.fabric.microsoft.com/.default"
        )

    @patch("fabrictesting.fabric_api.api_access.InteractiveBrowserCredential")
    def test_get_personal_fabric_token_exception(self, mock_interactive_credential):
        """
        Test the get_personal_fabric_token function
        when no token is returned (exception raised).
        """
        # Mocking the InteractiveBrowserCredential to return a token object with None
        mock_instance = mock_interactive_credential.return_value
        mock_instance.get_token.return_value.token = None

        # Check if the exception is raised when token is None
        with self.assertRaises(Exception) as context:
            get_personal_fabric_token("mock_tenant_id")

        self.assertEqual(str(context.exception), "Token string was none")

    @patch("fabrictesting.fabric_api.api_access.ClientSecretCredential")
    def test_get_client_fabric_token_success(self, mock_client_secret_credential):
        """
        Test the get_client_fabric_token function when a valid token is returned.
        """
        # Mocking the token
        mock_token = MagicMock()
        mock_token.token = "mock_client_token_string"

        # Mocking the ClientSecretCredential to return a mocked token
        mock_instance = mock_client_secret_credential.return_value
        mock_instance.get_token.return_value = mock_token

        # Call the function and assert the result
        token = get_client_fabric_token(
            "mock_tenant_id", "mock_client_id", "mock_client_secret"
        )
        self.assertEqual(token, "mock_client_token_string")

        # Assert that get_token was called with the correct scope
        mock_instance.get_token.assert_called_once_with(
            "https://api.fabric.microsoft.com/.default"
        )

    @patch("fabrictesting.fabric_api.api_access.ClientSecretCredential")
    def test_get_client_fabric_token_exception(self, mock_client_secret_credential):
        """
        Test the get_client_fabric_token function
        when no token is returned (exception raised).
        """
        # Mocking the ClientSecretCredential to return a token object with None
        mock_instance = mock_client_secret_credential.return_value
        mock_instance.get_token.return_value.token = None

        # Check if the exception is raised when token is None
        with self.assertRaises(Exception) as context:
            get_client_fabric_token(
                "mock_tenant_id", "mock_client_id", "mock_client_secret"
            )

        self.assertEqual(str(context.exception), "Token string was none")
