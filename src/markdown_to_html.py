
# Markdown to HTML Converter

import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_to_blocks import BlockType, markdown_to_blocks, block_to_block_type
from text_to_html import text_node_to_html_node
from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter, split_nodes_links, split_nodes_images, text_to_textnode
from extract_images_links import extract_markdown_images, extract_markdown_links

def markdown_to_html_node(markdown):

    full_html_doc = []

    blocks = markdown_to_blocks(markdown)

    for block in blocks:

        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            
            heading = heading_helper(block)
            full_html_doc.append(heading)

        elif block_type == BlockType.CODE:

            code = code_helper(block)
            full_html_doc.append(code)

        elif block_type == BlockType.QUOTE:
            
            quote = quote_helper(block)
            full_html_doc.append(quote)
        
        elif block_type == BlockType.UNORDERED_LIST:
            
            unordered_list = unordered_list_helper(block)
            full_html_doc.append(unordered_list)
        
        elif block_type == BlockType.ORDERED_LIST:
            
            ordered_list = ordered_list_helper(block)
            full_html_doc.append(ordered_list)
        
        else:
            
            paragraph = paragraph_helper(block)
            full_html_doc.append(paragraph)

    final_doc = full_doc_parent_node(full_html_doc)
    return final_doc


def text_to_children(text):

    node = text_to_textnode(text)

    html_node = [text_node_to_html_node(n) for n in node]

    return html_node

def heading_helper(text):

    level = text.count('#')

    stripped_text = text.lstrip('#').strip()

    node = text_to_children(stripped_text)

    parent_node = ParentNode(f"h{level}", node)
    return parent_node

def code_helper(text):

    stripped_text = text.strip('```').lstrip()

    node = TextNode(stripped_text, TextType.TEXT)
    html_node = text_node_to_html_node(node)

    child_node = ParentNode("code", [html_node])
    parent_node = ParentNode("pre", [child_node])

    return parent_node

def quote_helper(text):


    stripped_text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)

    split_node = stripped_text.split('\n')

    node = text_to_children('\n'.join(split_node))

    parent_node = ParentNode("blockquote", node)

    return parent_node

def unordered_list_helper(text):

    stripped_text = re.sub(r'^[-*+]\s+', '', text, flags=re.MULTILINE)

    split_node = stripped_text.split('\n')

    child_node = []

    for item in split_node:
        node = text_to_children(item)
        child_node.append(ParentNode("li", node))

    parent_node = ParentNode("ul", child_node)
    return parent_node

def ordered_list_helper(text):

    stripped_text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)

    split_node = stripped_text.split('\n')

    child_node = []

    for item in split_node:
        node = text_to_children(item)
        child_node.append(ParentNode("li", node))

    parent_node = ParentNode("ol", child_node)
    return parent_node

def paragraph_helper(text):

    node = text_to_children(text.replace('\n', ' '))

    parent_node = ParentNode("p", node)
    return parent_node

def full_doc_parent_node(full_doc):
    
    parent_node = ParentNode("div", full_doc)
    return parent_node