import re

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    block = []
    for line in markdown.split("\n\n"):
        if line.strip():
            block.append(line.strip())
    return block


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_ordered_list:
        return ol_to_html_node(block)
    if block_type == block_type_unordered_list:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block: 
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Something wrong with {block}")
    text = block[level+1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith('```') or not block.endswith('```'):
        raise ValueError("Invalid Code Block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    new_lines = []
    lines = block.split("\n")
    for line in lines:
        if not line.startswith('>'):
            raise ValueError("Invalid blockquote")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def ol_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def block_to_block_type(block):
    if re.match(r'^[#]{1,6}\s+', block):
        return block_type_heading
    elif block.startswith('```') and block.endswith('```'):
        return block_type_code
    elif all(line.startswith('>') for line in block.splitlines() if line.strip()):
        return block_type_quote
    elif all((line.startswith('*') or line.startswith('-')) for line in block.splitlines() if line.strip()):
        return block_type_unordered_list
    elif check_ordered_list_format(block):
        return block_type_ordered_list
    else:
        return block_type_paragraph


def check_ordered_list_format(block):
    # Remove empty or whitespace-only lines
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    expected_number = 1  # Start with 1 as the first expected number

    for line in lines:
        # Check if the line starts with 'expected_number.' followed by a space
        if not line.startswith(f"{expected_number}. "):
            return False
        expected_number += 1  # Increment the expected number for the next line

    return True


def count_leading_hashes(s):
    match = re.match(r'^([#]{1,6})\s+', s)
    if match:
        return len(match.group(1))
    else:
        return 0
