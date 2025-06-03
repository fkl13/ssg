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
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != text_type_text:
            new_nodes.append(n)
            continue

        text = n.text
        images = extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append(n)
            continue

        for image in images:
            sections = text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")

            if sections[0] != "":
                node = TextNode(sections[0], text_type_text)
                new_nodes.append(node)
            node = TextNode(image[0], text_type_image, image[1])
            new_nodes.append(node)

            text = sections[1]

        if text != "":
            new_nodes.append(TextNode(text, text_type_text))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != text_type_text:
            new_nodes.append(n)
            continue

        text = n.text
        links = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(n)
            continue

        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")

            if sections[0] != "":
                node = TextNode(sections[0], text_type_text)
                new_nodes.append(node)
            node = TextNode(link[0], text_type_link, link[1])
            new_nodes.append(node)

            text = sections[1]

        if text != "":
            new_nodes.append(TextNode(text, text_type_text))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "_", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
