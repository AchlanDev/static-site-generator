
# Extract Markdown Images

import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_html import text_node_to_html_node

def extract_markdown_images(text):

    image_pattern = r"!\[([^\]]*)\]\(([^)\s]+)\)"
    matches = re.findall(image_pattern, text)
    
    image_nodes = []
    for alt_text, url in matches:
        image_nodes.append((alt_text, url))
    
    return image_nodes

def extract_markdown_links(text):

    link_pattern = r"(?<![!])\[([^\]]*)\]\(([^)\s]+)\)"
    matches = re.findall(link_pattern, text)
    
    link_nodes = []
    for alt_text, url in matches:
        link_nodes.append((alt_text, url))
    
    return link_nodes

def extract_title(markdown):

    split_lines = markdown.split("\n")

    for line in split_lines:

        stripped_line = line.strip()

        if stripped_line.startswith("# "):
            return stripped_line[2:].strip()

    else:
        raise Exception("No title found.")