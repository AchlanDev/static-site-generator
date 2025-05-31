import unittest

from splitnodes import split_nodes_delimiter
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_html import text_node_to_html_node

class TestSplitNodes(unittest.TestCase):

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)


    def test_split_nodes_invalid_syntax(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_multiple_delimiters(self):
        node = TextNode("This is text with a `code block` and another `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[3].text, "code block")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)

    def test_split_nodes_no_delimiter(self):
        node = TextNode("This is text without delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text without delimiters")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)