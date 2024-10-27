import unittest

from block import *


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        block = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
* This is a list item
* This is another list item""",
        ]
        self.assertListEqual(markdown_to_blocks(block), blocks)

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("paragraph"), block_type_paragraph)
        self.assertEqual(block_to_block_type("# header"), block_type_heading)
        self.assertEqual(block_to_block_type("### header"), block_type_heading)
        code = """```
code
```"""
        self.assertEqual(block_to_block_type(code), block_type_code)

        quote = """> quote
> quote"""
        self.assertEqual(block_to_block_type(quote), block_type_quote)

        unordered_list = """*ulist
- ulst"""
        self.assertEqual(block_to_block_type(unordered_list), block_type_ulist)

        ordered_list = """1. olist
22. olst"""
        self.assertEqual(block_to_block_type(ordered_list), block_type_olist)


if __name__ == "__main__":
    unittest.main()
