import unittest

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


if __name__ == "__main__":
    unittest.main()