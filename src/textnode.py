from enum import Enum

class TextType(Enum):
    NORMAL_TEXT = "Normal text"
    ITALIC_TEXT = "*Italic text*"
    BOLD_TEXT = "**Bold text**"
    CODE_TEXT = "`Code text`"
    LINK_TEXT = "[Link text](https://example.com)"
    IMAGE_TEXT = "![Image text](https://example.com/image.jpg)"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        if not isinstance(value, type(self)):
            return False
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )


    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'