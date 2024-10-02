import unittest
from unittest.mock import mock_open, patch

from fabrictesting.utilities.load_fetch_url_log import load_fetch_url


class TestLoadFetchUrl(unittest.TestCase):
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="https://api.fabric.microsoft.com/v1/workspaces/xxxx-yyyy-zzzz/items/aaaa-bbbb/jobs/instances/cccc-dddd",
    )
    def test_load_fetch_url_success(self, mock_file):
        """
        Test load_fetch_url reads and returns the URL from the file successfully.
        """
        # Act: Call the function
        result = load_fetch_url("fetch_url.txt")

        # Assert: Ensure the correct URL is returned
        expected_url = "https://api.fabric.microsoft.com/v1/workspaces/xxxx-yyyy-zzzz/items/aaaa-bbbb/jobs/instances/cccc-dddd"
        self.assertEqual(result, expected_url)

        # Ensure the file was opened correctly
        mock_file.assert_called_once_with("fetch_url.txt", "r")

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_load_fetch_url_empty_file(self, mock_file):
        """
        Test load_fetch_url returns an empty string when the file is empty.
        """
        # Act: Call the function
        result = load_fetch_url("fetch_url.txt")

        # Assert: Ensure an empty string is returned
        self.assertEqual(result, "")

        # Ensure the file was opened correctly
        mock_file.assert_called_once_with("fetch_url.txt", "r")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_fetch_url_file_not_found(self, mock_file):
        """
        Test load_fetch_url raises FileNotFoundError when the file does not exist.
        """
        # Act & Assert: Ensure FileNotFoundError is raised
        with self.assertRaises(FileNotFoundError):
            load_fetch_url("fetch_url.txt")

        # Ensure the file was attempted to be opened
        mock_file.assert_called_once_with("fetch_url.txt", "r")
