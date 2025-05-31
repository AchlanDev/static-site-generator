import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    # HTMLNode tests

    def test_repr(self):
        node = HTMLNode("span", "This is a span", [], {"style": "color: red;"})
        expected_repr = "HTMLNode(span, This is a span, [], {'style': 'color: red;'})"
        self.assertEqual(repr(node), expected_repr)

    def test_props_to_html(self):
        node = HTMLNode("tag", "value", [], {"class": "container", "id": "main", "style": "color: blue;"})
        result = node.props_to_html()
        self.assertIn('class="container"', result)
        self.assertIn('id="main"', result)
        self.assertIn('style="color: blue;"', result)

    def test_props_to_html_no_props(self):
        node = HTMLNode("tag", "value", [])
        result = node.props_to_html()
        self.assertEqual("", result)

    def test_props_to_html_empty_props(self):
        node = HTMLNode("tag", "value", [], {})
        result = node.props_to_html()
        self.assertEqual("", result)

class TestLeafNode(unittest.TestCase):

    # LeafNode tests

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "This is a span")
        self.assertEqual(node.to_html(), "<span>This is a span</span>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(value="This is a text without a tag")
        self.assertEqual(node.to_html(), "This is a text without a tag")



class TestParentNode(unittest.TestCase):

    # ParentNode tests

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>", )

    def test_parent_to_html(self):
        test_child = [LeafNode("p", "Child 1")]
        node = ParentNode("div", test_child, {"class": "parent"})
        self.assertEqual(node.to_html(), '<div class="parent"><p>Child 1</p></div>')

    def test_parent_to_html_no_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode(None, "Testing")])
            node.to_html()

    def test_parent_to_html_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", None)
            node.to_html()