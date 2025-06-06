import unittest

from extract_images_links import extract_markdown_images, extract_markdown_links, extract_title
from splitnodes import split_nodes_delimiter
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_html import text_node_to_html_node

class TestExtractImagesLinks(unittest.TestCase):

    def test_extract_markdown_images(self):

        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")

        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):

        matches = extract_markdown_links("This is text with a [link](https://example.com) and ![image](https://i.imgur.com/zjjcJKZ.png)")
        
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_multiple_images(self):

        matches = extract_markdown_images("This is text with an ![image1](https://i.imgur.com/zjjcJKZ.png) and another ![image2](https://i.imgur.com/another.png)")
        
        self.assertListEqual([("image1", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/another.png")], matches)

    def test_multiple_links(self):

        matches = extract_markdown_links("This is text with a [link1](https://example.com) and another [link2](https://example.org)")
        
        self.assertListEqual([("link1", "https://example.com"), ("link2", "https://example.org")], matches)

    def test_no_images_or_links(self):

        matches = extract_markdown_images("This is text without images")
        self.assertListEqual([], matches)

        matches = extract_markdown_links("This is text without links")
        self.assertListEqual([], matches)

    def test_invalid_markdown(self):
        matches = extract_markdown_images("This is an invalid ![image without closing parenthesis")
        self.assertListEqual([], matches)
        matches = extract_markdown_links("This is an invalid [link without closing parenthesis")
        self.assertListEqual([], matches)


class TestExtractTitle(unittest.TestCase):

    def test_extract_title(self):
        markdown = "# This is a title\n\nThis is some content."
        title = extract_title(markdown)
        self.assertEqual(title, "This is a title")

    def test_no_title(self):
        markdown = "This is some content without a title."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertTrue("No title found." in str(context.exception))

    def test_empty_markdown(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertTrue("No title found." in str(context.exception))

    def test_title_with_leading_spaces(self):
        markdown = "   # This is a title with leading spaces\n\nThis is some content."
        title = extract_title(markdown)
        self.assertEqual(title, "This is a title with leading spaces")