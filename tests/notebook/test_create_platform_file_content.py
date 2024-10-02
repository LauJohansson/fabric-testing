import json
import unittest
from unittest.mock import patch

from fabrictesting.notebook.create import create_platform_file_content


class TestCreatePlatformFileContent(unittest.TestCase):
    @patch("uuid.uuid4")
    def test_create_platform_file_content(self, mock_uuid):
        # Arrange: Mock the UUID to return a predictable value
        mock_uuid.return_value.hex = "1234567890abcdef"

        display_name = "Test Notebook"
        description = "This is a test notebook description."

        # Act: Call the function
        result = create_platform_file_content(display_name, description)

        # Parse the result to JSON for easier inspection
        result_json = json.loads(result)

        # Assert: Check if the UUID, displayName, and description are correct
        self.assertEqual(result_json["config"]["logicalId"], "1234567890abcdef")
        self.assertEqual(result_json["metadata"]["displayName"], display_name)
        self.assertEqual(result_json["metadata"]["description"], description)
        self.assertEqual(
            result_json["$schema"],
            "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        )
        self.assertEqual(result_json["config"]["version"], "2.0")
