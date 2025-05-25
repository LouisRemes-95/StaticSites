import sys
from pathlib import Path

from copy_directory_and_content import *
from htmlnode import markdown_to_html_node
from markdown_processing import extract_title


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_directory_and_content("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)



    
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if Path(dir_path_content).suffix == ".md":
        generate_page(dir_path_content, template_path, Path(dest_dir_path).with_suffix(".html"), basepath)
    elif Path(dir_path_content).is_dir():
        for element in os.listdir(dir_path_content):
            generate_pages_recursive(os.path.join(dir_path_content, element), template_path, os.path.join(dest_dir_path, element), basepath)

main()