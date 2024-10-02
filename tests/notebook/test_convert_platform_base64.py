import base64
import unittest

from fabrictesting.notebook.create import convert_platform_into_inlinebase64


class TestConvertPlatformIntoInlineBase64(unittest.TestCase):
    def test_convert_platform_into_inlinebase64(self):
        # Arrange: Define the platform content to be encoded
        platform_content = '{"metadata": {"displayName": "Test Platform"}}'

        # Manually encode the expected result in Base64
        expected_base64 = base64.b64encode(platform_content.encode("utf-8")).decode(
            "utf-8"
        )

        # Act: Call the function
        result = convert_platform_into_inlinebase64(platform_content)

        # Assert: Check if the output matches the expected Base64 encoded string
        self.assertEqual(result, expected_base64)
