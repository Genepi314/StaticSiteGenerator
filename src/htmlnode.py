class HTMLNode():
    def __init__(
        self, 
        tag: str | None = None, 
        value: str | None = None, 
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> None:
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        props_html = ""
        if self.props is not None:
            for prop in self.props:
                props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    

class LeafNode(HTMLNode):
    def __init__(
            self, tag: str | None, value: str, props: dict[str, str] | None = None
        ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        elif self.tag is None:
            return f"{self.value}"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
    
class ParentNode(HTMLNode):
    def __init__(
        self, 
        tag: str, 
        children: list["HTMLNode"], 
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None:
            raise ValueError("Parent node is missing values for children")
        html_string = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children:
            html_string += f"{node.to_html()}"
        html_string += f"</{self.tag}>"
        return html_string