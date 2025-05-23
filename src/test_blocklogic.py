import unittest

from blocklogic import markdown_to_blocks, block_to_block_type, BlockType

class Text_blocklogic(unittest.TestCase):
    def test_markdown_to_blocks_1(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_2(self):
        md = """
This is **bolded** paragraph


        This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line    





   - This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading_1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_2(self):
        block = "###### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_3(self):
        block = "####### This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_1(self):
        block = "```This is code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_2(self):
        block = "``This is not code```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_3(self):
        block = "```This is code````"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote_1(self):
        block = """> This is a quote
> And still is a quote"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_2(self):
        block = """> This is not a quote
Due to this line"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote_3(self):
        block = """> This is a quote
>And still is a quote"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_4(self):
        block = """> This is a quote
>> And still is a quote"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list_1(self):
        block = """- This is a unordered list
- And still is a unordered list"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_2(self):
        block = """- This is a not unordered list
-Due to this line"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_1(self):
        block = """1. This is an ordered list
2. And still is"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_2(self):
        block = """1. This is not an ordered list
2 Due to this line"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_3(self):
        block = """1. This is not an ordered list
3. Due to this line"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_4(self):
        block = """1. This is not an ordered list
2.Due to this line"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()