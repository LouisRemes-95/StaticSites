from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    html_node = HTMLNode("a", "This is some text", props = {"href": "https://www.google.com", "target": "_blank"})
    print(html_node.props_to_html())

main()