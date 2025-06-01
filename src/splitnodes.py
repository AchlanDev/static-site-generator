
# Split Nodes Delimiter

import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_html import text_node_to_html_node
from extract_images_links import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    new_nodes = []
    
    for node in old_nodes:

        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        
        split_text = node.text.split(delimiter)

        if len(split_text) % 2 == 0:
            raise ValueError("invalid Markdown syntax")

        for index, text in enumerate(split_text):
            if len(text) == 0:
                continue
            
            if index % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes

def split_nodes_links(old_nodes):

    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted_links = extract_markdown_links(node.text)

        if len(extracted_links) == 0:
            if '[' in node.text:
                raise ValueError("invalid Markdown syntax")
            new_nodes.append(node)
            continue

        else:
            remaining_text = node.text

            for extracted_link in extracted_links:

                alt_text, url = extracted_link

                full_link_markdown = f"[{alt_text}]({url})"

                parts = remaining_text.split(full_link_markdown, 1)

                if len(parts[0]) > 0:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))

                new_nodes.append(TextNode(alt_text, TextType.LINK, url))

                remaining_text = parts[1]

            if len(remaining_text) > 0:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_images(old_nodes):

    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted_links = extract_markdown_images(node.text)

        if len(extracted_links) == 0:
            if '![' in node.text:
                raise ValueError("invalid Markdown syntax")
            new_nodes.append(node)
            continue

        else:
            remaining_text = node.text

            for extracted_link in extracted_links:

                alt_text, url = extracted_link

                full_image_markdown = f"![{alt_text}]({url})"

                parts = remaining_text.split(full_image_markdown, 1)

                if len(parts[0]) > 0:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))

                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

                remaining_text = parts[1]

            if len(remaining_text) > 0:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes