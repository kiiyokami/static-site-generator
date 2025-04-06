import re

from node.textnode import TextNode, TextType
from node.htmlnode import LeafNode

def text_node_to_html_node(text_node):
    tag_mapping = {
        TextType.TEXT: (None, None),
        TextType.BOLD: ("b", None),
        TextType.ITALIC: ("i", None),
        TextType.CODE: ("code", None),
        TextType.LINK: ("a", {"href": text_node.url}),
        TextType.IMAGE: ("img", {"src": text_node.url, "alt": text_node.text})
    }
    
    tag, attributes = tag_mapping.get(text_node.text_type)
    text = "" if text_node.text_type == TextType.IMAGE else text_node.text
    return LeafNode(tag, text, attributes)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
            
        for i, section in enumerate(sections):
            if not section:
                continue
            new_nodes.append(
                TextNode(section, text_type if i % 2 else TextType.TEXT)
            )
            
    return new_nodes

def text_to_textnodes(text):
    delimiters = [
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
        ("`", TextType.CODE)
    ]
    
    nodes = [TextNode(text, TextType.TEXT)]
    for delimiter, text_type in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
        
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches 

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches
    

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        text = old_node.text
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(old_node)
            continue
            
        current_position = 0
        for image in images:
            image_markdown = f"![{image[0]}]({image[1]})"
            image_position = text.find(image_markdown, current_position)
            
            if image_position == -1:
                raise ValueError("Invalid markdown, image not closed")
                
            if image_position > current_position:
                new_nodes.append(
                    TextNode(text[current_position:image_position], TextType.TEXT)
                )
                
            new_nodes.append(
                TextNode(image[0], TextType.IMAGE, image[1])
            )
            
            current_position = image_position + len(image_markdown)
        
        if current_position < len(text):
            new_nodes.append(
                TextNode(text[current_position:], TextType.TEXT)
            )
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        text = old_node.text
        links = extract_markdown_links(text)
        if not links:
            new_nodes.append(old_node)
            continue
            
        current_position = 0
        for link in links:
            link_markdown = f"[{link[0]}]({link[1]})"
            link_position = text.find(link_markdown, current_position)
            
            if link_position == -1:
                raise ValueError("Invalid markdown, link not closed")
                
            if link_position > current_position:
                new_nodes.append(
                    TextNode(text[current_position:link_position], TextType.TEXT)
                )
                
            new_nodes.append(
                TextNode(link[0], TextType.LINK, link[1])
            )
            
            current_position = link_position + len(link_markdown)
        
        if current_position < len(text):
            new_nodes.append(
                TextNode(text[current_position:], TextType.TEXT)
            )
            
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

