import unittest
from unittest.mock import patch
from io import StringIO

from textnode import TextNode, TextType
from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_print(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            html_node = HTMLNode("a", "This is some text", props = {"href": "https://www.google.com"})
            print(html_node)
            self.assertEqual(fake_out.getvalue(), "HTMLNODE(a, This is some text, None, {'href': 'https://www.google.com'})\n")

    def test_print_parent(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            html_node = HTMLNode("a", "This is some text", props = {"href": "https://www.google.com"})
            html_node_parent = HTMLNode("a", "This is some text", [html_node], {"href": "https://www.google.com"})
            print(html_node_parent)
            self.assertEqual(fake_out.getvalue(), "HTMLNODE(a, This is some text, [HTMLNODE(a, This is some text, None, {'href': 'https://www.google.com'})], {'href': 'https://www.google.com'})\n")

    def test_props_to_html(self):
        html_node = HTMLNode("a", "This is some text", props = {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(html_node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_no_props(self):
        html_node = HTMLNode("a", "This is some text")
        self.assertEqual(html_node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "Click me!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html(self):
        node = ParentNode("p",
        [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        ],)
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent_to_html_props(self):
        node = ParentNode("p",
        [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        ], {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<p href="https://www.google.com" target="_blank"><b>Bold text</b>Normal text</p>')

    def test_text_node_to_html_node_TEXT(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_LINK(self):
        node = TextNode("Click me!", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_text_node_to_html_node_IMAGE(self):
        node = TextNode("Nice?", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "Nice?"})

    def test_block_to_tag_1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_tag(block), "h1")

    def test_block_to_tag_2(self):
        block = "###### This is a heading"
        self.assertEqual(block_to_tag(block), "h6")

    def test_block_to_tag_3(self):
        block = "```This is code```"
        self.assertEqual(block_to_tag(block), "pre")

    def test_block_to_tag_4(self):
        block = """> This is a quote
> And still is a quote"""
        self.assertEqual(block_to_tag(block), "blockquote")

    def test_block_to_tag_5(self):
        block = """- This is a unordered list
- And still is a unordered list"""
        self.assertEqual(block_to_tag(block), "ul")

    def test_block_to_tag_6(self):
        block = """1. This is an ordered list
2. And still is"""
        self.assertEqual(block_to_tag(block), "ol")

    def test_block_to_tag_7(self):
        block = """1. This is an ordered list
2.And still is"""
        self.assertEqual(block_to_tag(block), "p")

    def test_text_to_children_1(self):
        block = "# This is a heading"
        self.assertEqual(text_to_children(block), [LeafNode(None, "This is a heading")])

    def test_text_to_children_2(self):
        block = "```This is code```"
        self.assertEqual(text_to_children(block), [LeafNode("code", "This is code")])

    def test_text_to_children_3(self):
        block = """> This is a quote
> And still is a quote"""
        self.assertEqual(text_to_children(block), [LeafNode(None, "This is a quote And still is a quote")])

    def test_text_to_children_4(self):
        block = """- This is a unordered list
- And still is a unordered list"""
        self.assertEqual(text_to_children(block), [ParentNode("li", [LeafNode(None, "This is a unordered list")]), ParentNode("li", [LeafNode(None, "And still is a unordered list")])])

    def test_text_to_children_5(self):
        block = """1. This is an ordered list
2. And still is an ordered list"""
        self.assertEqual(text_to_children(block), [ParentNode("li", [LeafNode(None, "This is an ordered list")]), ParentNode("li", [LeafNode(None, "And still is an ordered list")])])

    def test_text_to_children_6(self):
        block = """1. This is an ordered list
2.And still is"""
        self.assertEqual(text_to_children(block), [LeafNode(None, "1. This is an ordered list 2.And still is")])

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

    def test_list_quote_image(self):
        md = """
- First item
- Second item with **bold**
- Third item

> This is a quote

![Alt text](https://example.com/image.png)
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ul><li>First item</li><li>Second item with <b>bold</b></li><li>Third item</li></ul><blockquote>This is a quote</blockquote><p><img src=\"https://example.com/image.png\" alt=\"Alt text\"/></p></div>",
    )

    

if __name__ == "__main__":
    unittest.main()
