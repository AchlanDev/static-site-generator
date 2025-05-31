

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("not implemented")

    def props_to_html(self):
        
        attribute_list = []

        if self.props is None:
            return ""

        for attribute_name, attribute_value in self.props.items():
            attribute_list.append(f" {attribute_name}=\"{attribute_value}\"")

        return "".join(attribute_list)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"



class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("value error")
        if self.tag == None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"



class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        # print(f"Debug: self.children = {self.children}")
        # print(f"Debug: type of self.children = {type(self.children)}")
        if self.tag == None:
            raise ValueError("tag error")
        if self.children == None:
            raise ValueError("children error")
        
        full_node = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            full_node += child.to_html()

        full_node += f"</{self.tag}>"

        return full_node