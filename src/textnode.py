from enum import Enum
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, target):
        return (self.text == target.text and 
                self.text_type == target.text_type and
                self.url == target.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            nodes.append(old_node)
        elif old_node.text.count(delimiter) % 2:
            raise Exception("No pair of delimiter in node")
        else:
            for iter, split_node in enumerate(old_node.text.split(delimiter)):
                if split_node:
                    if iter  % 2:
                        nodes.append(TextNode(split_node, text_type))
                    else:
                        nodes.append(TextNode(split_node, old_node.text_type))
    return nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            nodes.append(old_node)
        else:
            images = extract_markdown_images(old_node.text)
            reamining_text = old_node.text
            for image in images:
                text, reamining_text = reamining_text.split(f"![{image[0]}]({image[1]})", 1)
                if text:
                    nodes.append(TextNode(text, TextType.TEXT))
                nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            if reamining_text:
                nodes.append(TextNode(reamining_text, TextType.TEXT))
    return nodes

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_link(old_nodes):
    nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            nodes.append(old_node)
        else:
            links = extract_markdown_links(old_node.text)
            reamining_text = old_node.text
            for link in links:
                text, reamining_text = reamining_text.split(f"[{link[0]}]({link[1]})", 1)
                if text:
                    nodes.append(TextNode(text, TextType.TEXT))
                nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            if reamining_text:
                nodes.append(TextNode(reamining_text, TextType.TEXT))
    return nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

                