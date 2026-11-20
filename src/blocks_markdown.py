from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode, LeafNode

from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    new_blocks = []
    split_markdown = markdown.split("\n\n")
    for block in split_markdown:
        block = block.strip()
        if block:
            new_blocks.append(block)
    return new_blocks

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown: str) -> ParentNode:
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        new_node = block_to_html_node(block, block_type)
        children.append(new_node)
    return ParentNode("div", children)


def text_to_children(text:str) -> list[LeafNode]:
    leafnodes = []
    tnodes = text_to_textnodes(text)
    for tnode in tnodes:
        leafnodes.append(text_node_to_html_node(tnode))
    return leafnodes


def block_to_html_node(block, block_type) -> ParentNode:

    match block_type:

        case BlockType.PARAGRAPH:
            flat_text = " ".join(block.split("\n"))
            return ParentNode("p", text_to_children(flat_text))
        
        case BlockType.HEADING:
            count_heading = len(block) - len(block.lstrip("#"))
            clean_block = block[count_heading:].lstrip()
            return ParentNode(f"h{count_heading}", text_to_children(clean_block))
        
        case BlockType.QUOTE:
            lines = block.split("\n")
            clean_lines = []
            for line in lines:
                if not line.startswith(">"):
                    raise ValueError('Missing ">" inside quote block')
                clean_lines.append(line[1:].lstrip())
            clean_block = " ".join(clean_lines)
            return ParentNode("blockquote", text_to_children(clean_block))

        case BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            items = []
            for line in lines:
                if not line.startswith("- "):
                    raise ValueError('Missing "- " in list')
                items.append(ParentNode("li", text_to_children(line[2:])))
            return ParentNode("ul", items)

        case BlockType.ORDERED_LIST:
            lines = block.split("\n")
            items = []
            for line in lines:
                split_line = line.split(". ", 1)
                items.append(ParentNode("li", text_to_children(split_line[1])))
            return ParentNode("ol", items)

        case BlockType.CODE:
            clean_block = block[4:-3]
            text_node = TextNode(clean_block, TextType.PLAIN)
            leaf_node = text_node_to_html_node(text_node)
            first_parent = ParentNode("code", [leaf_node])
            return ParentNode("pre", [first_parent])

        case _:
            raise ValueError(f"unsupported block type: {block_type}")
