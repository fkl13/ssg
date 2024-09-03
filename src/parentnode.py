from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must NOT have a value")
        if self.children == None:
            raise ValueError("ParentNode must have at least one child")
        children = ""
        for c in self.children:
            children += c.to_html()
        return f'<{self.tag}{self.props_to_html()}>{children}</{self.tag}>'
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
