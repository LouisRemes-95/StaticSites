import unittest
from unittest.mock import patch

from textnode import *


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
        self.assertEqual(split_nodes_delimiter([node, node], "_", TextType.CODE), node2)

    def test_split_nodes_delimiter_7(self):
        node = TextNode("_", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "_", TextType.CODE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_2_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and  ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_Empty(self):
        matches = extract_markdown_images("This is text with no image")
        self.assertListEqual([], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with an [image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_2_links(self):
        matches = extract_markdown_links("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and [image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links_empty(self):
        matches = extract_markdown_links("This is text with no link")
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT),
                            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                            TextNode(" and another ", TextType.TEXT),
                            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),],
                            new_nodes,)

    def test_split_images_2(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                            TextNode(" and another ", TextType.TEXT),
                            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),],
                            new_nodes,)

    def test_split_images_3(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),],
                            new_nodes,)

    def test_split_images_4(self):
        node = TextNode(
            "![](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),],
                            new_nodes,)

    def test_split_images_5(self):
        node = TextNode(
            "![]()",
            TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("", TextType.IMAGE, ""),],
                            new_nodes,)

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT),
                            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                            TextNode(" and another ", TextType.TEXT),
                            TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),],
                            new_nodes,)

    def test_split_links_2(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                            TextNode(" and another ", TextType.TEXT),
                            TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),],
                            new_nodes,)

    def test_split_links_3(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)[second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                            TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),],
                            new_nodes,)

    def test_split_links_4(self):
        node = TextNode(
            "[](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),],
                            new_nodes,)

    def test_split_links_5(self):
        node = TextNode(
            "[]()",
            TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("", TextType.LINK, ""),],
                            new_nodes,)

    def test_text_to_textnodes_1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = [TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                ]
        self.assertEqual(text_to_textnodes(text), nodes)

    def test_text_to_textnodes_2(self):
        text = "**text**![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        nodes = [TextNode("text", TextType.BOLD),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                ]
        self.assertEqual(text_to_textnodes(text), nodes)

    def test_text_to_textnodes_3(self):
        text = "**text![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_text_to_textnodes_4(self):
        text = ""
        nodes = []
        self.assertEqual(text_to_textnodes(text), nodes)

    def test_text_to_textnodes_5(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg"
        nodes = [TextNode("![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), nodes)


if __name__ == "__main__":
    unittest.main()
