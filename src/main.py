
# Static Site Generator Main Module
# Run: source venv/bin/activate in ./static-site-generator

import os
import shutil
from textnode import TextNode, TextType
from generate_html import generate_page

def main():

    print("Copying static files to public directory...")

    result = static_to_public("static", "public")

    print("Files copied successfully.")

    # for item in os.walk("static"):
    #     for name in item[2]:
    #         print(os.path.join(item[0], name))

    print("Starting static site generation...")

    generate_page(from_path="content/index.md", template_path="template.html", dest_path="public/index.html")

    for item in os.walk("content"):
        for name in item[2]:
            generate_page(from_path=f"{item[0]}/{name}", template_path="template.html", dest_path=f"public/{item[0].removeprefix("content/")}/{name.replace('.md', '.html')}")

    print("Static site generated.")

    return result

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