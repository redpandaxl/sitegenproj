import unittest
from markdown_blocks import block_to_block_type, markdown_to_blocks


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_typei_UL(self):
        sample_text = """
* This is a line starting with star
- And this one starts with a dash
*Another star-starting line
"""
        self.assertEqual(block_to_block_type(sample_text), "unordered_list")

    def test_block_to_type_OL(self):
        block = """
        1. Test 1
        2. Test 2
        3. Test 3
        """
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_block_to_type_bad_OL(self):
        block = """
        1. Test 1
        Test 2
        3. Test 3
        """
        self.assertEqual(block_to_block_type(block), "paragraph")


if __name__ == "__main__":
    unittest.main()
