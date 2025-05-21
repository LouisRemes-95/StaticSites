class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return "".join(map(lambda prop: " " + prop[0] + '="' + prop[1]  + '"', self.props.items()))
    
    def __repr__(self):
        return f"HTMLNODE({self.tag}, {self.value}, {self.children}, {self.props})"
    


