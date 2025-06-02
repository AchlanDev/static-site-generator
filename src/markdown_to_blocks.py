
# Markdown to Blocks Converter

import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):

    if not markdown:
        return []

    if len(markdown) == 1 and markdown[0] == ' ':
        return []

    lines = markdown.split('\n\n')

    lines = [line.strip() for line in lines if line.strip() != '']

    return lines

def block_to_block_type(markdown):

    lines = markdown.split('\n')
    lines = [line.strip() for line in lines if line.strip() != '']
    i = 1

    if re.match(r'^#{1,6} ', lines[0]):
        return BlockType.HEADING

    elif lines[0].startswith('```') and lines[-1].endswith('```'):
        return BlockType.CODE

    elif lines[0].startswith('>'):
        for line in lines:
            
            if not line.startswith('>'):
                break
        else:
            return BlockType.QUOTE

    elif lines[0].startswith('- '):
        for line in lines:

            if not line.startswith('- '):
                break
        else:
            return BlockType.UNORDERED_LIST

    elif re.match(r'^\d+\. ', lines[0]):
        for line in lines:

            if not line.startswith(f'{i}. '):
                break

            i += 1
        else:
            return BlockType.ORDERED_LIST

    else:
        return BlockType.PARAGRAPH