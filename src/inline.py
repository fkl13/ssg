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


def split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        images = extract_markdown_images(n.text)
        text = n.text
        for image in images:
            sections = text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")

            nodes = []
            for i, sec in enumerate(sections):
                if sec == "":
                    continue
                if i % 2 == 0:
                    node = TextNode(sec, text_type_text)
                    nodes.append(node)
                    node = TextNode(image[0], text_type_image, image[1])
                    nodes.append(node)
                else:
                    text = sec
            new_nodes.extend(nodes)
    if len(new_nodes) == 0:
        return old_nodes
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        links = extract_markdown_links(n.text)
        text = n.text
        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")

            nodes = []
            for i, sec in enumerate(sections):
                if sec == "":
                    continue
                if i % 2 == 0:
                    node = TextNode(sec, text_type_text)
                    nodes.append(node)
                    node = TextNode(link[0], text_type_link, link[1])
                    nodes.append(node)
                else:
                    text = sec
            new_nodes.extend(nodes)
    if len(new_nodes) == 0:
        return old_nodes
    return new_nodes
