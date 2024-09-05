import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParent(unittest.TestCase):
    def test_to_html_no_child(self):
        node = ParentNode( "p", [], )
        self.assertEqual(node.to_html(), '<p></p>')

    def test_to_html_one_child(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
            ],
        )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b></p>')

    def test_to_html_two_child(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "some text"),
            ],
        )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>some text</p>')

    def test_to_html_nested_parent(self):
        node = ParentNode(
            "div",
            [
                ParentNode("p", [LeafNode("b", "Bold text")]),
            ],
        )
        self.assertEqual(node.to_html(), '<div><p><b>Bold text</b></p></div>')

if __name__ == "__main__":
    unittest.main()