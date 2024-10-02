import base64
import unittest

from fabrictesting.notebook.create import convert_notebook_into_inlinebase64


class TestConvertNotebookIntoInlineBase64(unittest.TestCase):
    def test_convert_notebook_into_inlinebase64(self):
        # Arrange: Define test inputs and expected outputs
        notebook_content = "This is a test notebook content."

        # Manually encode the expected result in Base64
        expected_base64 = base64.b64encode(notebook_content.encode("utf-8")).decode(
            "utf-8"
        )

        # Act: Call the function
        result = convert_notebook_into_inlinebase64(notebook_content)

        # Assert: Check if the output matches the expected Base64 encoded string
        self.assertEqual(result, expected_base64)


if __name__ == "__main__":
    unittest.main()
