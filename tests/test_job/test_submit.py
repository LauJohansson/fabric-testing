import argparse
import unittest
from unittest.mock import MagicMock, call, patch

from fabrictesting.test_job.submit import submit, submit_args


class TestSubmitFlow(unittest.TestCase):
    @patch(
        "fabrictesting.test_job.submit.run_notebook",
        return_value={"status_code": 202, "fetch_url": "https://mock-fetch-url.com"},
    )
    @patch(
        "fabrictesting.test_job.submit.get_notebook_id", return_value="mock-notebook-id"
    )
    @patch("fabrictesting.test_job.submit.upload_notebook")
    @patch(
        "fabrictesting.test_job.submit.load_default_notebook",
        return_value="mock-notebook-content",
    )
    @patch(
        "fabrictesting.test_job.submit.create_platform_file_content",
        return_value="mock-platform-content",
    )
    @patch(
        "fabrictesting.test_job.submit.upload_folder_to_onelake",
        return_value="mock-folder-name",
    )
    @patch(
        "fabrictesting.test_job.submit.create_temp_folder_with_files",
        return_value=("mock-temp-dir", "mock-wheel-name", "mock-reqs.txt"),
    )
    @patch(
        "fabrictesting.test_job.submit.get_personal_fabric_token",
        return_value="mock-fabric-token",
    )
    @patch("fabrictesting.test_job.submit.save_fetch_url_log")
    @patch("builtins.print")  # Mock print statements
    @patch("time.sleep", return_value=None)  # Mock sleep to avoid actual delay
    def test_submit_full_flow_personal_account(
        self,
        mock_sleep,
        mock_print,
        mock_save_fetch_url_log,
        mock_get_personal_fabric_token,
        mock_create_temp_folder_with_files,
        mock_upload_folder_to_onelake,
        mock_create_platform_file_content,
        mock_load_default_notebook,
        mock_upload_notebook,
        mock_get_notebook_id,
        mock_run_notebook,
    ):
        """
        Test the full flow of the submit function for a personal account.
        """

        # Arrange: Set up the args
        args = MagicMock(
            tenant_id="mock-tenant-id",
            whl_path="mock-whl-path",
            tests_path="mock-tests-path",
            requirements_file="mock-reqs-path",
            workspace_name="mock-workspace-name",
            workspace_id="mock-workspace-id",
            lakehouse_name="mock-lakehouse-name",
            lakehouse_id="mock-lakehouse-id",
            output_log_file_path="mock-log-path",
            service_principal=False,
            client_id=None,
            client_secret=None,
        )

        # Act: Call the submit function
        fetch_url = submit(args)

        # Assert: Ensure that the functions were called in the
        # correct order and with the right parameters

        # Token fetching
        mock_get_personal_fabric_token.assert_called_once_with("mock-tenant-id")

        # Temp folder creation
        mock_create_temp_folder_with_files.assert_called_once_with(
            whl_path="mock-whl-path",
            tests_path="mock-tests-path",
            requirements_file="mock-reqs-path",
        )

        mock_create_platform_file_content.assert_called_once_with(
            display_name="mock-folder-name",
            description="This is a fabric-testing notebook",
        )

        # Folder upload
        mock_upload_folder_to_onelake.assert_called_once_with(
            temp_folder="mock-temp-dir",
            workspace_name="mock-workspace-name",
            lakehouse_name="mock-lakehouse-name",
        )

        # Notebook content creation
        mock_load_default_notebook.assert_called_once_with(
            lakehouse_id="mock-lakehouse-id",
            default_lakehouse_name="mock-lakehouse-name",
            default_lakehouse_workspace_id="mock-workspace-id",
            workspace_name="mock-workspace-name",
            submit_folder="mock-folder-name",
            wheel_name="mock-wheel-name",
            requirements_file_name="mock-reqs.txt",
            unittest_folder_name="tests",
        )

        # Notebook upload
        mock_upload_notebook.assert_called_once_with(
            display_name="mock-folder-name",
            description="This is a fabric-testing notebook",
            notebook_definition="mock-notebook-content",
            platform_definition="mock-platform-content",
            workspace_id="mock-workspace-id",
            token_string="mock-fabric-token",
        )

        # Get notebook ID
        mock_get_notebook_id.assert_called_once_with(
            notebook_name="mock-folder-name",
            workspace_id="mock-workspace-id",
            token_string="mock-fabric-token",
        )

        # Run notebook
        mock_run_notebook.assert_called_once_with(
            item_id="mock-notebook-id",
            workspace_id="mock-workspace-id",
            token_string="mock-fabric-token",
        )

        # Save fetch URL log
        mock_save_fetch_url_log.assert_called_once_with("https://mock-fetch-url.com")

        # Assert the returned URL is correct
        self.assertEqual(fetch_url, "https://mock-fetch-url.com")

        # Assert the correct print statements were made
        expected_print_calls = [
            call("Starting fabric-testing submit..."),
            call("Give Fabric API 5 seconds to upload notebook..."),
            call("Notebook triggered with status 202"),
            call("Notebook has the name: mock-folder-name"),
            call("Notebook has id mock-notebook-id"),
            call("Fetch results at https://mock-fetch-url.com"),
            call("Fabric-testing submit ran successfully!"),
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)


class TestSubmitArgsCombinations(unittest.TestCase):
    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            tenant_id="some-tenant-id",
            whl_path="mock-whl-path",
            tests_path="mock-tests-path",
            requirements_file="mock-reqs-path",
            workspace_name="mock-workspace-name",
            workspace_id="mock-workspace-id",
            lakehouse_name="mock-lakehouse-name",
            lakehouse_id="mock-lakehouse-id",
            output_log_file_path=None,
            service_principal=True,
            client_id="mock-client-id",
            client_secret="mock-client-secret",
        ),
    )
    @patch("fabrictesting.test_job.submit.validate_args")
    def test_args_with_service_principal(self, mock_validate_args, mock_parse_args):
        """
        Test parsing args when service_principal is True and both client_id and client_secret are provided.
        """
        # Act
        args = submit_args()

        # Assert
        self.assertEqual(args.tenant_id, "some-tenant-id")
        self.assertTrue(args.service_principal)
        self.assertEqual(args.client_id, "mock-client-id")
        self.assertEqual(args.client_secret, "mock-client-secret")
        self.assertEqual(args.workspace_name, "mock-workspace-name")
        mock_validate_args.assert_called_once_with(args, unittest.mock.ANY)

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            tenant_id="some-tenant-id",
            whl_path="mock-whl-path",
            tests_path="mock-tests-path",
            requirements_file="mock-reqs-path",
            workspace_name="mock-workspace-name",
            workspace_id="mock-workspace-id",
            lakehouse_name="mock-lakehouse-name",
            lakehouse_id="mock-lakehouse-id",
            output_log_file_path=None,
            service_principal=True,
            client_id=None,
            client_secret=None,
        ),
    )
    def test_args_missing_client_id_and_secret(self, mock_parse_args):
        """
        Test args with service_principal=True but missing client_id and client_secret.
        This should trigger a validation error.
        """
        # Act & Assert: Now SystemExit should be raised because validate_args will trigger a parser error
        with self.assertRaises(SystemExit):  # argparse raises SystemExit on error
            submit_args()

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            tenant_id="some-tenant-id",
            whl_path="mock-whl-path",
            tests_path="mock-tests-path",
            requirements_file=None,
            workspace_name="mock-workspace-name",
            workspace_id="mock-workspace-id",
            lakehouse_name="mock-lakehouse-name",
            lakehouse_id="mock-lakehouse-id",
            output_log_file_path="mock-log-path",
            service_principal=False,
            client_id=None,
            client_secret=None,
        ),
    )
    @patch("fabrictesting.test_job.submit.validate_args")
    def test_args_without_service_principal(self, mock_validate_args, mock_parse_args):
        """
        Test args without service principal.
        """
        # Act
        args = submit_args()

        # Assert: Ensure the args are parsed correctly without service principal
        self.assertEqual(args.tenant_id, "some-tenant-id")
        self.assertFalse(args.service_principal)
        self.assertIsNone(args.client_id)
        self.assertIsNone(args.client_secret)
        self.assertEqual(args.whl_path, "mock-whl-path")
        self.assertEqual(args.output_log_file_path, "mock-log-path")
        mock_validate_args.assert_called_once_with(args, unittest.mock.ANY)

    @patch("fabrictesting.test_job.submit.validate_args")
    def test_missing_args(self, mock_validate_args):
        """
        Test args with multiple required arguments missing.
        This should raise a SystemExit as argparse detects missing required args.
        """
        # Act & Assert: Expect SystemExit due to missing required arguments
        test_args = [
            "--service-principal",
            "False",
            # We intentionally do not provide required arguments like --tenant-id, --workspace-name, etc.
        ]

        with patch("sys.argv", ["submit.py"] + test_args):
            with self.assertRaises(SystemExit):
                submit_args()
