from textnode import TextType, text_to_textnodes, TextNode
from blocklogic import *

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        return "".join(map(lambda prop: " " + prop[0] + '="' + prop[1]  + '"', self.props.items()))
    
    def __eq__(self, target):
        return (self.tag == target.tag and 
                self.value == target.value and
                self.children == target.children and
                self.props == target.props)
    
    def __repr__(self):
        return f"HTMLNODE({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, props = props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode has no value")
        if not self.tag:
            return self.value
        
        # Handle self-closing (void) HTML tags
        void_elements = {"img"}
        if self.tag in void_elements:
            return f"<{self.tag}{self.props_to_html()}/>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, children = children, props = props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode has no tag")
        if not self.children:
            raise ValueError("ParentNode has no children")
        return f"<{self.tag}{self.props_to_html()}>{''.join(map(lambda child: child.to_html(), self.children))}</{self.tag}>"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Incorrect TextNode type")
        
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    first_children = []
    for block in blocks:
        first_children.append(ParentNode(block_to_tag(block), text_to_children(block)))
    return ParentNode("div", first_children)

def block_to_tag(text):
    block_type = block_to_block_type(text)
    match block_type:
        case BlockType.HEADING:
            return f"h{len(text) - len(text.lstrip("#"))}"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case BlockType.CODE:
            return "pre"
        case BlockType.PARAGRAPH:
            return "p"
        case _:
            raise Exception("Incorrect block type")

def text_to_children(text):
    block_type = block_to_block_type(text)
    match block_type:
        case BlockType.HEADING:
            text = text.lstrip("# ")
            return text_to_html_nodes(text)
        case BlockType.QUOTE:
            text = " ".join(line.strip()[2:] for line in text.split("\n"))
            return text_to_html_nodes(text)
        case BlockType.UNORDERED_LIST:
            items = [line.strip()[2:] for line in text.split("\n")]
            return items_to_children(items)
        case BlockType.ORDERED_LIST:
            items = [line.strip()[3:] for line in text.split("\n")]
            return items_to_children(items)
        case BlockType.PARAGRAPH:
            return text_to_html_nodes(text)
        case BlockType.CODE:
            return [text_node_to_html_node(TextNode(text[3:-3].lstrip(), TextType.CODE))]
        case _:
            raise Exception("Incorrect block type")

def text_to_html_nodes(text):
    return [text_node_to_html_node(text_node) for text_node in text_to_textnodes(text)]

def items_to_children(items):
    children = []
    for item in items:
        children.append(ParentNode("li", text_to_html_nodes(item)))
    return children