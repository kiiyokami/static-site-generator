import unittest

from src.node.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    node1 = HTMLNode(None, None, None, None)
    node = HTMLNode(tag="p", value="Hello World", children=None)
    node3 = HTMLNode('img', None, 'src', 'https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg')
    node4 = HTMLNode('p', 'Test Text', 'id', 'test id')

    def raise_to_html_error(self):
        with self.assertRaises(ValueError):
            self.node1.to_html()

    def print_node(self):
        print(self.__repr__())

    def test_props_to_html_2(self):
        node = HTMLNode(tag="div", props={"class": "container", "id": "main"})
        expected_output = ' class="container" id="main"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_when_props_is_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_none_props(self):
        node_with_none_props = HTMLNode(tag="div", value="Test", children=None, props=None)
        result = node_with_none_props.props_to_html()
        self.assertEqual(result, "", "props_to_html should return an empty string when props is None")

if __name__ == "__main__":
    unittest.main()
