
# HTML Page Generator

from markdown_to_html import markdown_to_html_node
from extract_images_links import extract_title
import os
import shutil
from pathlib import Path


def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")

    dest_path = Path(dest_path)

    contents = Path(from_path).read_text(encoding='utf-8')

    template = Path(template_path).read_text(encoding='utf-8')

    contents_html = markdown_to_html_node(contents)
    contents_html_str = contents_html.to_html()

    title = extract_title(contents)

    first_replace = template.replace("{{ Title }}", title)
    full_html = first_replace.replace("{{ Content }}", contents_html_str)

    if os.path.dirname(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding='utf-8') as f:
        f.write(full_html)