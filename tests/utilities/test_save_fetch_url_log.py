import unittest
from unittest.mock import mock_open, patch

from fabrictesting.utilities.save_fetch_url_log import save_fetch_url_log


class TestSaveFetchUrlLog(unittest.TestCase):
    """
    Test Plan:
    Test saving a valid URL to a file:

    1: Simulate writing a valid URL to the file and
    ensure that the correct data is written.
    Test saving an empty URL to a file:

    2: Simulate writing an empty URL to the file
    and ensure that an empty string is written.
    Test handling of file writing errors:

    3: Simulate an error during the file write operation
     and ensure the function raises an appropriate error.
    """

    @patch("builtins.open", new_callable=mock_open)
    def test_save_fetch_url_log_success(self, mock_file):
        """
        Test save_fetch_url_log successfully writes the URL to the file.
        """
        # Arrange: URL to be written
        fetch_url = "https://api.fabric.microsoft.com/v1/workspaces/xxxx-yyyy-zzzz/items/aaaa-bbbb/jobs/instances/cccc-dddd"

        # Act: Call the function
        save_fetch_url_log(fetch_url, "fetch_url.txt")

        # Assert: Ensure the file was opened in write mode and the URL was written
        mock_file.assert_called_once_with("fetch_url.txt", "w")
        mock_file().write.assert_called_once_with(fetch_url)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_fetch_url_log_empty_url(self, mock_file):
        """
        Test save_fetch_url_log successfully writes an empty URL to the file.
        """
        # Arrange: Empty URL to be written
        fetch_url = ""

        # Act: Call the function
        save_fetch_url_log(fetch_url, "fetch_url.txt")

        # Assert: Ensure the file was opened in
        # write mode and the empty string was written
        mock_file.assert_called_once_with("fetch_url.txt", "w")
        mock_file().write.assert_called_once_with(fetch_url)

    @patch("builtins.open", side_effect=OSError("Failed to open file"))
    def test_save_fetch_url_log_failure(self, mock_file):
        """
        Test save_fetch_url_log raises an exception if writing to the file fails.
        """
        # Arrange: URL to be written
        fetch_url = "https://api.fabric.microsoft.com/v1/workspaces/xxxx-yyyy-zzzz/items/aaaa-bbbb/jobs/instances/cccc-dddd"

        # Act & Assert: Ensure that an exception is raised
        with self.assertRaises(OSError) as context:
            save_fetch_url_log(fetch_url, "fetch_url.txt")

        self.assertIn("Failed to open file", str(context.exception))

        # Ensure the file was attempted to be opened
        mock_file.assert_called_once_with("fetch_url.txt", "w")


if __name__ == "__main__":
    unittest.main()
