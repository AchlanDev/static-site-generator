
import unittest

from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
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

    def test_markdown_to_blocks_empty(self):
        md = ""

        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single_line(self):
        md = "This is a single line paragraph"

        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line paragraph"])

    def test_markdown_to_blocks_multiple_empty_lines(self):
        md = "\n\n\nThis is a paragraph after multiple empty lines\n\n"

        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph after multiple empty lines"])

class TestBlocktoBlockType(unittest.TestCase):

    # def test_block_to_block_type(self):
    #     md = 



    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        self.assertEqual(block_to_block_type("```\ncode block\n```"), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Item 2"), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("2. Second item"), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)

    def test_ordered_list_block(self):
        md = """
1. First item
2. Second item
3. Third item
        """
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.ORDERED_LIST)

    def test_code_block(self):
        md = """
```python
def hello():

    print("world")
```
"""
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.CODE)

    def test_quote_block(self):
        md = """
> This is a quote.
>
> This is still part of the quote.
"""
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.QUOTE)

    def test_invalid_quote_block(self):
        md = """
> First line
Second line
> Third line
"""
        blocks = block_to_block_type(md)
        self.assertNotEqual(blocks, BlockType.QUOTE)

    def test_invalid_ordered_list_block(self):
        md = """
1. First item
2. Second item
Not a list item
4. Fourth item
"""
        blocks = block_to_block_type(md)
        self.assertNotEqual(blocks, BlockType.ORDERED_LIST)