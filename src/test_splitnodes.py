import unittest

from splitnodes import split_nodes_delimiter, split_nodes_links, split_nodes_images, text_to_textnode
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

class TestSplitNodesLinks(unittest.TestCase):

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example.org)",
            TextType.TEXT
            )

        new_nodes = split_nodes_links([node])

        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("This is text without links", TextType.TEXT)
        new_nodes = split_nodes_links([node])

        self.assertListEqual([node], new_nodes)

    def test_split_links_invalid_syntax(self):
        node = TextNode("This is text with a [link without closing parenthesis", TextType.TEXT)

        with self.assertRaises(ValueError):
            split_nodes_links([node])

    def test_split_links_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_links([node])

        self.assertListEqual([node], new_nodes)
    
    def test_split_links_only_links(self):
        node = TextNode(
            "[link1](https://example.com) [link2](https://example.org)",
            TextType.TEXT
        )
        new_nodes = split_nodes_links([node])

        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "https://example.com"),
                TextNode(" ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )

    def test_split_links_mixed_content(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and some text and a [link](https://example.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_links([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and some text and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

class TestSplitNodesImages(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
            )

        new_nodes = split_nodes_images([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("This is text without images", TextType.TEXT)
        new_nodes = split_nodes_images([node])

        self.assertListEqual([node], new_nodes)

    def test_split_images_invalid_syntax(self):
        node = TextNode("This is text with an ![image without closing parenthesis", TextType.TEXT)

        with self.assertRaises(ValueError):
            split_nodes_images([node])

    def test_split_images_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_images([node])

        self.assertListEqual([node], new_nodes)

    def test_split_images_only_images(self):
        node = TextNode(
            "![image1](https://i.imgur.com/zjjcJKZ.png) ![image2](https://i.imgur.com/another.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_images([node])

        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/another.png"),
            ],
            new_nodes,
        )

    def test_split_images_mixed_content(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and some text and a [link](https://example.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_images([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and some text and a [link](https://example.com)", TextType.TEXT),
            ],
            new_nodes,
        )

class TestTexttoTextNode(unittest.TestCase):

    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnode(text)

        self.assertEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        , nodes)

    def test_invalid_text_to_textnode(self):
        text = "This is **text** with an _italic word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg and a [link](https://boot.dev)"

        with self.assertRaises(ValueError):
            text_to_textnode(text)

    def test_invalid_text_to_textnode(self):
        text = "This is **text** with an italic word_ and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a link](https://boot.dev)"

        with self.assertRaises(ValueError):
            text_to_textnode(text)

    def test_empty_text_to_textnode(self):
        text = ""
        nodes = text_to_textnode(text)

        self.assertEqual([], nodes)