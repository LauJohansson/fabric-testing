import argparse
import unittest
from unittest.mock import patch

from fabrictesting.test_job.fetch import fetch, fetch_args


class TestFetchArgs(unittest.TestCase):
    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            service_principal=True,
            tenant_id="some-tenant-id",
            client_id="some-client-id",
            client_secret="some-client-secret",
            retry_after=60,
            fetch_url_log_file_path=None,
            url="https://example.com/fetch-url",
        ),
    )
    @patch("fabrictesting.test_job.fetch.validate_args")
    def test_fetch_args_service_principal(self, mock_validate_args, mock_parse_args):
        """
        Test fetch_args when the service principal
        is provided with valid client_id and client_secret.
        """
        # Act
        args = fetch_args()

        # Assert
        self.assertEqual(args.tenant_id, "some-tenant-id")
        self.assertEqual(args.client_id, "some-client-id")
        self.assertEqual(args.client_secret, "some-client-secret")
        self.assertEqual(args.url, "https://example.com/fetch-url")
        mock_validate_args.assert_called_once_with(args, unittest.mock.ANY)

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            service_principal=False,
            tenant_id="some-tenant-id",
            client_id=None,
            client_secret=None,
            retry_after=30,
            fetch_url_log_file_path="mock_fetch_url.txt",
            url=None,
        ),
    )
    @patch("fabrictesting.test_job.fetch.validate_args")
    def test_fetch_args_personal_account(self, mock_validate_args, mock_parse_args):
        """
        Test fetch_args for personal account
        (without service principal) and a fetch URL from log file.
        """
        # Act
        args = fetch_args()

        # Assert
        self.assertEqual(args.tenant_id, "some-tenant-id")
        self.assertIsNone(args.client_id)
        self.assertIsNone(args.client_secret)
        self.assertEqual(args.retry_after, 30)
        self.assertEqual(args.fetch_url_log_file_path, "mock_fetch_url.txt")
        self.assertIsNone(args.url)
        mock_validate_args.assert_called_once_with(args, unittest.mock.ANY)


class TestFetchFunction(unittest.TestCase):
    @patch("fabrictesting.test_job.fetch.poll_notebook_run_status")
    @patch(
        "fabrictesting.test_job.fetch.load_fetch_url",
        return_value="https://example.com/fetch-url",
    )
    @patch(
        "fabrictesting.test_job.fetch.get_personal_fabric_token",
        return_value="personal-token",
    )
    def test_fetch_personal_account(
        self, mock_get_token, mock_load_fetch_url, mock_poll_notebook
    ):
        """
        Test fetch function for personal account
        with URL loaded from fetch_url_log_file_path.
        """
        # Arrange
        args = argparse.Namespace(
            service_principal=False,
            tenant_id="some-tenant-id",
            client_id=None,
            client_secret=None,
            retry_after=60,
            fetch_url_log_file_path="mock_fetch_url.txt",
            url=None,
        )

        # Act
        fetch(args)

        # Assert: Ensure the correct token fetching and polling calls are made
        mock_get_token.assert_called_once_with("some-tenant-id")
        mock_load_fetch_url.assert_called_once_with("mock_fetch_url.txt")
        mock_poll_notebook.assert_called_once_with(
            fetch_url="https://example.com/fetch-url",
            retry_after=60,
            token_string="personal-token",
        )

    @patch("fabrictesting.test_job.fetch.poll_notebook_run_status")
    @patch(
        "fabrictesting.test_job.fetch.get_client_fabric_token",
        return_value="service-principal-token",
    )
    def test_fetch_service_principal(self, mock_get_token, mock_poll_notebook):
        """
        Test fetch function for service principal with a direct URL provided.
        """
        # Arrange
        args = argparse.Namespace(
            service_principal=True,
            tenant_id="some-tenant-id",
            client_id="some-client-id",
            client_secret="some-client-secret",
            retry_after=120,
            fetch_url_log_file_path=None,
            url="https://example.com/fetch-url",
        )

        # Act
        fetch(args)

        # Assert: Ensure the correct token fetching and polling calls are made
        mock_get_token.assert_called_once_with(
            "some-tenant-id", "some-client-id", "some-client-secret"
        )
        mock_poll_notebook.assert_called_once_with(
            fetch_url="https://example.com/fetch-url",
            retry_after=120,
            token_string="service-principal-token",
        )

    @patch(
        "fabrictesting.test_job.fetch.get_personal_fabric_token",
        return_value="mock-personal-token",
    )
    @patch("fabrictesting.test_job.fetch.poll_notebook_run_status")
    @patch("sys.exit")
    def test_fetch_success_exit_code(
        self, mock_exit, mock_poll_notebook, mock_get_token
    ):
        """
        Test fetch function exits with code 0 when status_code is 200.
        """
        # Arrange
        args = argparse.Namespace(
            service_principal=False,
            tenant_id="some-tenant-id",
            client_id=None,
            client_secret=None,
            retry_after=60,
            fetch_url_log_file_path=None,
            url="https://example.com/fetch-url",
        )
        mock_poll_notebook.return_value = {"status_code": 200}

        # Act
        fetch(args)

        # Assert: Ensure sys.exit(0) is called on success
        mock_exit.assert_called_once_with(0)

    @patch(
        "fabrictesting.test_job.fetch.get_personal_fabric_token",
        return_value="mock-personal-token",
    )
    @patch("fabrictesting.test_job.fetch.poll_notebook_run_status")
    @patch("sys.exit")
    def test_fetch_failure_exit_code(
        self, mock_exit, mock_poll_notebook, mock_get_token
    ):
        """
        Test fetch function exits with code -1 when status_code is not 200.
        """
        # Arrange
        args = argparse.Namespace(
            service_principal=False,
            tenant_id="some-tenant-id",
            client_id=None,
            client_secret=None,
            retry_after=60,
            fetch_url_log_file_path=None,
            url="https://example.com/fetch-url",
        )
        mock_poll_notebook.return_value = {"status_code": 500}

        # Act
        fetch(args)

        # Assert: Ensure sys.exit(-1) is called on failure
        mock_exit.assert_called_once_with(-1)
