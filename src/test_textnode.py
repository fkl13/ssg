import unittest

from textnode import TextNode
from textnode import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italics")
        self.assertNotEqual(node, node2)

    def test_not_eq2(self):
        node = TextNode("This is a text node 1", "bold", None)
        node2 = TextNode("This is a text node 2", "bold", None)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertEqual(node, node2)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_to_leaf_node(self):
        node = TextNode("This is a text node", "text")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, None)
        self.assertEqual(leaf.value, "This is a text node")

    def test_bold_to_leaf_node(self):
        node = TextNode("This is a text node", "bold")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, "b")
        self.assertEqual(leaf.value, "This is a text node")

    def test_italic_to_leaf_node(self):
        node = TextNode("This is a text node", "italic")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, "i")
        self.assertEqual(leaf.value, "This is a text node")

    def test_code_to_leaf_node(self):
        node = TextNode("This is a text node", "code")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, "code")
        self.assertEqual(leaf.value, "This is a text node")

    def test_link_to_leaf_node(self):
        node = TextNode("This is a text node", "link", "https://www.boot.dev")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, "a")
        self.assertEqual(leaf.value, "This is a text node")
        self.assertEqual(leaf.props, {"href": "https://www.boot.dev"})

    def test_image_to_leaf_node(self):
        node = TextNode("This is a text node", "image", "https://www.boot.dev")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, "img")
        self.assertEqual(leaf.value, "")
        self.assertEqual(leaf.props, {"src": "https://www.boot.dev", "alt": "This is a text node"})

if __name__ == "__main__":
    unittest.main()