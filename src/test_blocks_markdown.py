import unittest

from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
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

    def test_markdown_to_blocks_newlines(self):
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

    def test_block_to_block_type_heading(self):
        self.assertEqual(
            BlockType.HEADING,
            block_to_block_type("###### This is a very important heading")
        )
        # The following would be better raising an exception
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("######This is not a very important heading")
        )
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("####### This is not a very important heading either")
        )

    def test_block_to_block_type_quote(self):
        self.assertEqual(
            BlockType.CODE,
            block_to_block_type("```print(`Hello, World`)```")
        )

    def test_block_to_block_type_quote(self):
        self.assertEqual(
            BlockType.QUOTE,
            block_to_block_type(">This is a quote")
        )
        self.assertEqual(
            BlockType.QUOTE,
            block_to_block_type("> This is also a quote")
        )
        self.assertEqual(
            BlockType.QUOTE,
            block_to_block_type(">>>>> And this too")
        )

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(
            BlockType.UNORDERED_LIST,
            block_to_block_type(
"""- This is
- an unordered
- list"""
        )
            )
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type(
"""
- Watch out !
- This is not
- an unordered list"""
            )
        )
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type(
"""- Watch out !

- an unordered list"""
            )
        )
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type(
"""- Watch out !
-This is not
- an unordered list"""
            )
        )

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(
            BlockType.ORDERED_LIST,
            block_to_block_type(
"""1. First
2. Second
3. Third"""
            )
        )
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type(
"""
1. First
2. Second
3. Third"""
            )
        )
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type(
"""1. First
2. Second
4. Third???"""
            )
        )
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type(
"""0. This is
1. weirdly
2. not okay"""
            )
        )


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_quoteblock(self):
        md = """
> The bear knows
> where the honey is
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>The bear knows where the honey is</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
- Honey
- Fresh _salmon_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Honey</li><li>Fresh <i>salmon</i></li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. Wake up. Stretch.
2. Find **honey**
3. Nap
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Wake up. Stretch.</li><li>Find <b>honey</b></li><li>Nap</li></ol></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )