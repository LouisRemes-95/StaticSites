from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode

def main():
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(node.to_html())

main()