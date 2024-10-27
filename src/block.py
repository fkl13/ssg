import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code

    is_quote = True
    for l in lines:
        if not l.startswith(">"):
            is_quote = False
    if is_quote:
        return block_type_quote

    is_unordered_list = True
    for l in lines:
        if l.startswith("*") or l.startswith("-"):
            continue
        else:
            is_unordered_list = False
    if is_unordered_list:
        return block_type_ulist

    is_ordered_list = True
    for l in lines:
        if not re.match(r"^\d+\.", l):
            is_ordered_list = False
    if is_ordered_list:
        return block_type_olist

    return block_type_paragraph
