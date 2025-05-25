from copy_directory_and_content import *
from htmlnode import markdown_to_html_node
from markdown_processing import extract_title


def main():
    copy_directory_and_content("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
    
def generate_page(from_path, template_path, dest_path):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(template)



main()