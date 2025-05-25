from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import copy_directory_and_content


def main():
    copy_directory_and_content("static", "public")
    
def generate_page(from_path, template_path, dest_path):
    pass


main()