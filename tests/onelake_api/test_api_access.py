import unittest
from unittest.mock import MagicMock, patch

from fabrictesting.onelake_api.api_access import get_service_client


class TestGetServiceClient(unittest.TestCase):
    @patch("fabrictesting.onelake_api.api_access.DataLakeServiceClient")
    @patch("fabrictesting.onelake_api.api_access.DefaultAzureCredential")
    def test_get_service_client_success(
        self, mock_default_credential, mock_datalake_client
    ):
        """
        Test get_service_client successfully creates a DataLakeServiceClient.
        """
        # Arrange: Mock the return value of DefaultAzureCredential
        mock_credential_instance = MagicMock()
        mock_default_credential.return_value = mock_credential_instance

        # Arrange: Mock the return value of DataLakeServiceClient
        mock_service_client_instance = MagicMock()
        mock_datalake_client.return_value = mock_service_client_instance

        # Act: Call the function
        result = get_service_client()

        # Assert: Ensure the DataLakeServiceClient
        # was created with the expected arguments
        mock_datalake_client.assert_called_once_with(
            "https://onelake.dfs.fabric.microsoft.com",
            credential=mock_credential_instance,
        )
        self.assertEqual(result, mock_service_client_instance)

    @patch("fabrictesting.onelake_api.api_access.DataLakeServiceClient")
    @patch("fabrictesting.onelake_api.api_access.DefaultAzureCredential")
    def test_get_service_client_failure(
        self, mock_default_credential, mock_datalake_client
    ):
        """
        Test get_service_client when DataLakeServiceClient creation fails.
        """
        # Arrange: Mock DefaultAzureCredential to return a valid credential
        mock_credential_instance = MagicMock()
        mock_default_credential.return_value = mock_credential_instance

        # Arrange: Simulate an exception when creating DataLakeServiceClient
        mock_datalake_client.side_effect = Exception("Failed to create service client")

        # Act & Assert: Ensure that an exception is raised
        with self.assertRaises(Exception) as context:
            get_service_client()

        self.assertIn("Failed to create service client", str(context.exception))
        mock_datalake_client.assert_called_once_with(
            "https://onelake.dfs.fabric.microsoft.com",
            credential=mock_credential_instance,
        )


if __name__ == "__main__":
    unittest.main()
