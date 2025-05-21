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
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "Nice?"})
        # self.assertEqual(html_node.to_html(), '<img src="https://www.google.com" alt="Nice?"><\img>')

if __name__ == "__main__":
    unittest.main()
