import unittest
from unittest.mock import patch
from io import StringIO


from htmlnode import HTMLNode, LeafNode


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
        

if __name__ == "__main__":
    unittest.main()
