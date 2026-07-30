from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: "TextNode") -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    tag = None
    value = text_node.text
    props = None
    match text_node.text_type:
        case TextType.PLAIN:
            pass
        case TextType.BOLD:
            tag = "b"
        case TextType.ITALIC:
            tag = "i"
        case TextType.CODE:
            tag = "code"
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("invalid URL")
            tag = "a"
            props = {"href": text_node.url}
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("invalid URL")
            tag = "img"
            value = ""
            props = {"src": text_node.url, "alt": text_node.text}
        case _:
            raise ValueError("Not a valid text type")
    return LeafNode(tag, value, props)
