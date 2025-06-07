
# HTML Page Generator

from markdown_to_html import markdown_to_html_node
from extract_images_links import extract_title
import os
import shutil
from pathlib import Path


def generate_page(basepath, from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")

    dest_path = Path(dest_path)

    contents = Path(from_path).read_text(encoding='utf-8')

    template = Path(template_path).read_text(encoding='utf-8')

    contents_html = markdown_to_html_node(contents)
    contents_html_str = contents_html.to_html()

    title = extract_title(contents)

    first_replace = template.replace("{{ Title }}", title)
    second_replace = first_replace.replace("{{ Content }}", contents_html_str)
    third_repalce = second_replace.replace('href="', f'href="{basepath}')
    full_html = third_repalce.replace('src="', f'src="{basepath}')

    if os.path.dirname(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding='utf-8') as f:
        f.write(full_html)

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):

    def _generate_recursive(basepath, current_src, template_path, current_dst):

        for item in os.listdir(current_src):

            src_path = os.path.join(current_src, item)
            dst_path = os.path.join(current_dst, item)

            if os.path.isdir(src_path):
                print(f"Entering directory: {src_path}")
                os.makedirs(dst_path, exist_ok=True)
                _generate_recursive(basepath, src_path, template_path, dst_path)

            elif os.path.isfile(src_path) and src_path.endswith(".md"):
                print(f"Generating page from {src_path} to {dst_path}")
                generate_page(basepath, from_path=src_path, template_path=template_path, dest_path=dst_path.replace(".md", ".html"))

            elif os.path.isfile(src_path) and not src_path.endswith(".md"):
                print(f"Copying static file {src_path} to {dst_path}")
                shutil.copy2(src_path, dst_path)

    _generate_recursive(basepath, dir_path_content, template_path, dest_dir_path)