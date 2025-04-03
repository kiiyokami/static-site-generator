from src.node.htmlnode import LeafNode, ParentNode
from src.node.textnode import TextNode
import unittest

class TestParentNode(unittest.TestCase):
    def setUp(self):
        self.basic_tag = "div"
        self.basic_children = [TextNode("Hello, world!", 'bold')]
        self.basic_props = {"class": "container"}
        self.basic_node = ParentNode(
            self.basic_tag,
            self.basic_children,
            self.basic_props
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test___repr___(self):
        expected_repr = f"ParentNode({self.basic_tag}, {self.basic_children}, {self.basic_props})"
        self.assertEqual(repr(self.basic_node), expected_repr)

    def test_init_with_valid_inputs(self):
        tag = "div"
        children = [ParentNode("p", [])]
        props = {"class": "container"}

        parent_node = ParentNode(tag, children, props)

        self.assertEqual(parent_node.tag, tag)
        self.assertEqual(parent_node.children, children)
        self.assertEqual(parent_node.props, props)
        self.assertIsNone(parent_node.value)

    def test_to_html_with_none_tag(self):
        children = [ParentNode("p", [])]
        parent_node = ParentNode(None, children)

        with self.assertRaisesRegex(ValueError, "Tag is required"):
            parent_node.to_html()

    def test_to_html_with_none_children(self):
        parent_node = ParentNode("div", None)

        with self.assertRaisesRegex(ValueError, "Children is required"):
            parent_node.to_html()

    def test_to_html_with_none_tag_and_children(self):
        parent_node = ParentNode(None, None)

        with self.assertRaisesRegex(ValueError, "Tag is required"):
            parent_node.to_html()

if __name__ == '__main__':
    unittest.main()
