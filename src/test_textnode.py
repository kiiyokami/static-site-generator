import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        # Setup test cases
        node1 = TextNode("Bold Text", TextType.BOLD)
        node2 = TextNode("Bold Text", TextType.BOLD)  # Same as node1
        node3 = TextNode("Bold Text", TextType.ITALIC)  # Same text, different type
        node4 = TextNode("Different Text", TextType.BOLD)  # Different text, same type
        node5 = TextNode("Link Text", TextType.LINK, "https://example.com")
        
        # Test equality
        self.assertEqual(node1, node2)  # Same content and type should be equal
        self.assertNotEqual(node1, node3)  # Different type should not be equal
        self.assertNotEqual(node1, node4)  # Different text should not be equal
        
        # Test edge cases
        self.assertNotEqual(node1, None)  # Comparison with None
        self.assertNotEqual(node1, "Bold Text")  # Comparison with different type
        self.assertNotEqual(node1, node5)  # Comparison with node containing URL
        
        # Test reflexivity
        self.assertEqual(node1, node1)  # Object should equal itself


if __name__ == "__main__":
    unittest.main()