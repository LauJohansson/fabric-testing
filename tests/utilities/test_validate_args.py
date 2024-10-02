import argparse
import unittest
from unittest.mock import MagicMock

from fabrictesting.utilities.validate_args import validate_args


class TestValidateArgs(unittest.TestCase):
    """
    Test Plan:
    Test when both client_id and client_secret are provided:
    The function should pass without raising an error.

    Test when only client_id is provided without client_secret:
    The function should raise a validation error.

    Test when only client_secret is provided without client_id:
    The function should raise a validation error.

    Test when service_principal is provided without client_id and client_secret:
    The function should raise a validation error.

    Test when service_principal is provided with both client_id and client_secret:
    The function should pass without raising an error.
    """

    def setUp(self):
        # Create a mock parser to use in tests, and ensure it raises SystemExit on error
        self.mock_parser = MagicMock()
        self.mock_parser.error.side_effect = (
            SystemExit  # Simulate the behavior of argparse
        )

    def test_validate_args_success_with_client_id_and_secret(self):
        """
        Test validate_args passes when both client_id and client_secret are provided.
        """
        # Arrange: Set up the args
        args = argparse.Namespace(
            client_id="some-client-id",
            client_secret="some-client-secret",
            service_principal=False,
        )

        # Act & Assert: Call the function (should not raise an error)
        validate_args(args, self.mock_parser)
        self.mock_parser.error.assert_not_called()

    def test_validate_args_fail_missing_client_secret(self):
        """
        Test validate_args raises an error when client_id
        is provided without client_secret.
        """
        # Arrange: Set up the args
        args = argparse.Namespace(
            client_id="some-client-id", client_secret=None, service_principal=False
        )

        # Act & Assert: Call the function (should raise an error)
        with self.assertRaises(SystemExit):  # Now SystemExit should be raised
            validate_args(args, self.mock_parser)
        self.mock_parser.error.assert_called_once_with(
            "Both --client-id and --client-secret must be provided together."
        )

    def test_validate_args_fail_missing_client_id(self):
        """
        Test validate_args raises an error when client_secret
        is provided without client_id.
        """
        # Arrange: Set up the args
        args = argparse.Namespace(
            client_id=None, client_secret="some-client-secret", service_principal=False
        )

        # Act & Assert: Call the function (should raise an error)
        with self.assertRaises(SystemExit):  # Now SystemExit should be raised
            validate_args(args, self.mock_parser)
        self.mock_parser.error.assert_called_once_with(
            "Both --client-id and --client-secret must be provided together."
        )

    def test_validate_args_fail_service_principal_missing_client_id_and_secret(self):
        """
        Test validate_args raises an error when service_principal
        is true but client_id and client_secret are missing.
        """
        # Arrange: Set up the args
        args = argparse.Namespace(
            client_id=None, client_secret=None, service_principal=True
        )

        # Act & Assert: Call the function (should raise an error)
        with self.assertRaises(SystemExit):  # Now SystemExit should be raised
            validate_args(args, self.mock_parser)
        self.mock_parser.error.assert_called_once_with(
            "Expecting service principal but "
            "missing either --client-id or --client-secret."
        )

    def test_validate_args_success_service_principal_with_client_id_and_secret(self):
        """
        Test validate_args passes when service_principal
        is true and both client_id and client_secret are provided.
        """
        # Arrange: Set up the args
        args = argparse.Namespace(
            client_id="some-client-id",
            client_secret="some-client-secret",
            service_principal=True,
        )

        # Act & Assert: Call the function (should not raise an error)
        validate_args(args, self.mock_parser)
        self.mock_parser.error.assert_not_called()
