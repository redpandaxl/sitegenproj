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
