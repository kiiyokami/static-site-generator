import unittest
from src.node.htmlnode import LeafNode



class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test___init___1(self):
        tag = "div"
        value = "Test content"
        leaf_node = LeafNode(tag, value)
        self.assertEqual(leaf_node.value, value)

    def test___init___with_none_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test___repr___1(self):
        node = LeafNode("p", "Hello, world!", props={"class": "greeting"})
        expected_repr = "LeafNode(p, Hello, world!, {'class': 'greeting'})"
        self.assertEqual(repr(node), expected_repr)

    def test___repr___with_none_values(self):
        node = LeafNode(None, None, None)
        expected_repr = "LeafNode(None, None, None)"
        self.assertEqual(repr(node), expected_repr)

    def test_to_html_2(self):
        leaf = LeafNode(None, "Test Value")
        result = leaf.to_html()
        self.assertEqual(result, "Test Value")

    def test_to_html_3(self):
        leaf_node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            leaf_node.to_html()

    def test_to_html_raises_value_error_when_value_is_none(self):
        leaf_node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            leaf_node.to_html()

    def test_to_html_with_none_value(self):
        leaf_node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            leaf_node.to_html()


if __name__ == "__main__":
    unittest.main()
