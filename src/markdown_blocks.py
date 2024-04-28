import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    # Create a new function called markdown_to_blocks(markdown). It takes a raw Markdown string (representing a full document)
    # as input and returns a list of "block" strings.
    # Its job is to split the input string into distinct blocks and strip any leading or
    # trailing whitespace from each block. It should also remove any "empty" blocks due to excessive newlines.

    block = []
    for line in markdown.split("\n\n"):
        if line.strip():
            block.append(line.strip())
    return block


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
