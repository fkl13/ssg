import re

from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            nodes.append(old_node)
            continue

        if old_node.text.count(delimiter) % 2 == 1:
            raise Exception("Invalid markdown, not closed")

        split_nodes = []
        text_parts = old_node.text.split(delimiter)
        for i, part in enumerate(text_parts):
            if part == "":
                continue

            if i % 2 == 1:
                node = TextNode(part, text_type)
                split_nodes.append(node)
            else:
                node = TextNode(part, old_node.text_type)
                split_nodes.append(node)
        nodes.extend(split_nodes)
    return nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches