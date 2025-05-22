import unittest

from textnode import TextNode, TextType, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.boot.dev")
        self.assertEqual(node, node2)

    def test_neq_different_text(self):
        node = TextNode("This is a text node!", TextType.BOLD)
        node2 = TextNode("This is a text node?", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_different_text_with_url(self):
        node = TextNode("This is a text node!", TextType.BOLD, "www.boot.dev")
        node2 = TextNode("This is a text node?", TextType.BOLD, "www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_neq_different_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_different_type_with_url(self):
        node = TextNode("This is a text node", TextType.TEXT, "www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_neq_different_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.boot.devs")
        self.assertNotEqual(node, node2)

    def test_neq_all_different(self):
        node = TextNode("This is a text node!", TextType.TEXT, "www.boot.dev")
        node2 = TextNode("This is a text node?", TextType.BOLD, "www.boot.devs")
        self.assertNotEqual(node, node2)

    def test_split_nodes_delimiter_1(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = [TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), node2)

    def test_split_nodes_delimiter_2(self):
        node = TextNode("This is text with a _code block_ word", TextType.TEXT)
        node2 = [TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), node2)

    def test_split_nodes_delimiter_3(self):
        node = TextNode("This is text with a _code block_ word", TextType.TEXT)
        node2 = [TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.LINK),
                TextNode(" word", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.LINK), node2)

    def test_split_nodes_delimiter_4(self):
        node = TextNode("`code block` word", TextType.TEXT)
        node2 = [TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), node2)

    def test_split_nodes_delimiter_5(self):
        node = TextNode("`code block` word", TextType.TEXT)
        node2 = [TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),]
        node2.extend(node2)
        self.assertEqual(split_nodes_delimiter([node, node], "`", TextType.CODE), node2)

    def test_split_nodes_delimiter_6(self):
        node = TextNode("__", TextType.TEXT)
        node2 = []
        self.assertEqual(split_nodes_delimiter([node, node], "__", TextType.CODE), node2)


if __name__ == "__main__":
    unittest.main()
