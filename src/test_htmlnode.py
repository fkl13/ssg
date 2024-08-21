import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {"href": "https://www.boot.dev", "target":"_blank"}
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev" target="_blank"')

    def test_no_props(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), '')

    def test_prop_to_html(self):
        props = {"href": "https://www.boot.dev"}
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev"')


if __name__ == "__main__":
    unittest.main()