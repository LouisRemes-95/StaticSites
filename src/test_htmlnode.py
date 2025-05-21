import unittest
from unittest.mock import patch
from io import StringIO


from textnode import TextNode, TextType
from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()
