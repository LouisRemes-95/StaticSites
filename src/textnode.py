from enum import Enum

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
        elif delimiter not in old_node.text:
            raise Exception("No delimiter in node")
        else:
            for iter, split_node in enumerate(old_node.text.split(delimiter)):
                if split_node:
                    if iter  % 2:
                        nodes.append(TextNode(split_node, text_type))
                    else:
                        nodes.append(TextNode(split_node, old_node.text_type))
    return nodes
                