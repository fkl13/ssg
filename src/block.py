import re
from htmlnode import HTMLNode
from inline import text_to_textnodes
from parentnode import ParentNode
from textnode import TextNode, text_node_to_html_node, text_type_text

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


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        if type == block_type_paragraph:
            nodes.append(paragraph_to_node(block))
        elif type == block_type_heading:
            nodes.append(heading_to_node(block))
        elif type == block_type_code:
            nodes.append(code_to_node(block))
        elif type == block_type_quote:
            nodes.append(quote_to_node(block))
        elif type == block_type_olist:
            nodes.append(olist_to_node(block))
        elif type == block_type_ulist:
            nodes.append(ulist_to_node(block))

    return ParentNode("div", nodes, None)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, text_type_text)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
