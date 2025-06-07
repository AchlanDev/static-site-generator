
# Static Site Generator Main Module
# Run: source venv/bin/activate in ./static-site-generator

import os
import shutil
import sys
from textnode import TextNode, TextType
from generate_html import generate_pages_recursive

def main():

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    if not basepath == "/":
        output_dir = "docs"
    else:
        output_dir = "public"

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    print(f"Copying static files to {output_dir}...")

    static_to_public("static", output_dir)

    print("Files copied successfully.")

    print("Starting static site generation...")

    generate_pages_recursive(basepath, dir_path_content="content", template_path="template.html", dest_dir_path=output_dir)

    print("Static site generated.")

    return True

def static_to_public(static_dir, public_dir):

    if os.path.exists(public_dir):
        print(f"Removing existing public directory: {public_dir}")
        shutil.rmtree(public_dir)
    os.makedirs(public_dir)

    def _copy_static_files(current_src, current_dst):

        for item in os.listdir(current_src):

            print(os.path.join(current_src, item))

            src_path = os.path.join(current_src, item)
            dst_path = os.path.join(current_dst, item)

            if os.path.isdir(src_path):
                print(f"Entering directory: {src_path}")
                os.makedirs(dst_path, exist_ok=True)
                _copy_static_files(src_path, dst_path)
            else:
                print(f"Copying {item} from {src_path} to {dst_path}")
                shutil.copy2(src_path, dst_path)

    _copy_static_files(static_dir, public_dir)



if __name__ == "__main__":
    main()