from enum import Enum

import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    return [string.strip() for string in markdown.split("\n\n") if string.strip()]

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif block[0:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    elif all(line.strip().startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    elif all(line.strip().startswith("- ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif all(line.strip().startswith(f"{index+1}. ") for index, line in enumerate(block.split("\n"))):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH