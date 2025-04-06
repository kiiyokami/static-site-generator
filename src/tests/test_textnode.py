import unittest

from block_markdown import BlockType, block_to_blocktype, extract_title, markdown_to_html_node
from src.functions import *
from src.node.textnode import TextNode, TextType



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("Bold Text", TextType.BOLD)
        node2 = TextNode("Bold Text", TextType.BOLD)
        self.assertEqual(node1, node2)
    
    def test_eq_false(self):
        node1 = TextNode("Bold Text", TextType.BOLD)
        node2 = TextNode("Bold Text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)
    
    def none_type(self):
        node2 = TextNode("Bold Text", None)
        self.assertIsNone(node2.text_type)

    def link_test(self):
        node1 = TextNode("Link Text", TextType.LINK, "https://example.com")
        self.assertEqual(node1.url, "https://example.com")
    
    def code_test(self):
        node1 = TextNode("Code Text", TextType.CODE)
        self.assertEqual(node1.text_type, TextType.CODE)


    # TEST CASES FOR TEXTNODE TO HTML NODE

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_text_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
    
    def test_text_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
    
    def test_text_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props["href"], "https://example.com")
    
    def test_text_image(self):
        node = TextNode("This is an image text node", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://example.com/image.png")
        self.assertEqual(html_node.props["alt"], "This is an image text node")

    def invalid_text_type(self):
        node = TextNode("This is an invalid text node", "invalid_type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def split_node_testing(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = node.split_nodes_delimiter("code block", "`")
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def split_node_invalid_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        with self.assertRaises(ValueError):
            node.split_nodes_delimiter("code block", "invalid_delimiter")

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](XXXXXXXXXXXXXXX) and ![another](XXXXXXXXXXXXXXXXXXXXXXX)"
        expected = [("image", "XXXXXXXXXXXXXXX"), ("another", "XXXXXXXXXXXXXXXXXXXXXXX")]
        self.assertEqual(extract_markdown_images(text), expected)
    
    def rickroll(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertEqual(extract_markdown_links(text), expected)

    def no_extract_images(self):
        text = "This is text with no images"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def no_extract_links(self):
        text = "This is text with no links"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_split_nodes_image(self):
        test_text = "This is text with an ![image](https://i.imgur.com/ylOmKGA.jpeg) and another ![second image](https://i.imgur.com/ylOmKGA.jpeg)"
        node = TextNode(test_text, TextType.TEXT)
        
        new_nodes = split_nodes_image([node])
        
        expected_results = [
            ("This is text with an ", TextType.TEXT, None),
            ("image", TextType.IMAGE, "https://i.imgur.com/ylOmKGA.jpeg"),
            (" and another ", TextType.TEXT, None),
            ("second image", TextType.IMAGE, "https://i.imgur.com/ylOmKGA.jpeg")
        ]
        
        self.assertEqual(len(new_nodes), len(expected_results), 
                        f"Expected {len(expected_results)} nodes, got {len(new_nodes)}")
        
        for i, (node, (expected_text, expected_type, expected_url)) in enumerate(zip(new_nodes, expected_results)):
            self.assertEqual(node.text, expected_text, 
                            f"Node {i}: Text mismatch: expected '{expected_text}', got '{node.text}'")
            self.assertEqual(node.text_type, expected_type, 
                            f"Node {i}: Type mismatch for node '{node.text}'")
            self.assertEqual(node.url, expected_url, 
                            f"Node {i}: URL mismatch for node '{node.text}'")

    def test_split_nodes_link(self):
        test_text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        node = TextNode(test_text, TextType.TEXT)
        
        new_nodes = split_nodes_link([node])
        
        expected_results = [
            ("This is text with a ", TextType.TEXT, None),
            ("link", TextType.LINK, "https://www.example.com"),
            (" and ", TextType.TEXT, None),
            ("another", TextType.LINK, "https://www.example.com/another")
        ]
        
        self.assertEqual(len(new_nodes), len(expected_results), 
                        f"Expected {len(expected_results)} nodes, got {len(new_nodes)}")
        
        for i, (node, (expected_text, expected_type, expected_url)) in enumerate(zip(new_nodes, expected_results)):
            self.assertEqual(node.text, expected_text, 
                            f"Node {i}: Text mismatch: expected '{expected_text}', got '{node.text}'")
            self.assertEqual(node.text_type, expected_type, 
                            f"Node {i}: Type mismatch for node '{node.text}'")
            self.assertEqual(node.url, expected_url, 
                            f"Node {i}: URL mismatch for node '{node.text}'")

    def test_non_text_nodes_preserved(self):
        nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("Regular ![image](http://example.com)", TextType.TEXT),
            TextNode("Italic text", TextType.ITALIC)
        ]
        
        # Test image splitting
        result_nodes = split_nodes_image(nodes)
        self.assertEqual(result_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(result_nodes[-1].text_type, TextType.ITALIC)
        
        # Test link splitting
        result_nodes = split_nodes_link(nodes)
        self.assertEqual(result_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(result_nodes[-1].text_type, TextType.ITALIC)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)
    
    def test_markdown_to_blocks(self):
        markdown = """
            # This is a heading

            This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

            - This is the first list item in a list block
            - This is a list item
            - This is another list item
            """
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            """- This is the first list item in a list block
            - This is a list item
            - This is another list item"""
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_block_to_block_type(self):
        block = "# This is a heading"
        expected = BlockType.HEADING
        result = block_to_blocktype(block)
        self.assertEqual(result, expected)

        block = "###### This is a heading"
        expected = BlockType.HEADING
        result = block_to_blocktype(block)
        self.assertEqual(result, expected)

        block = "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."
        expected = BlockType.PARAGRAPH
        result = block_to_blocktype(block)
        self.assertEqual(result, expected)

        block = "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        expected = BlockType.UNORDERED_LIST
        result = block_to_blocktype(block)
        self.assertEqual(result, expected)

        block = "1. This is the first list item in a list block\n2. This is a list item\n3. This is another list item"
        expected = BlockType.ORDERED_LIST
        result = block_to_blocktype(block)
        self.assertEqual(result, expected)

        block = "```This is a code block```"
        expected = BlockType.CODE
        result = block_to_blocktype(block)
        self.assertEqual(result, expected)
    
    def test_paragraphs(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def extract_title_testt(self):
        text = "# Tolkien Fan Club"
        expected = "This is a title"
        self.assertEqual(extract_title(text), expected)




if __name__ == "__main__":
    unittest.main()