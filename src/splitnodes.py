
# Split Nodes Delimiter

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_html import text_node_to_html_node

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