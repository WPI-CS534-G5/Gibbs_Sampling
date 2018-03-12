class Node(object):
    """Node object in graph"""
    def __init__(self, arg):
        super(Node, self).__init__()
        self.arg = arg

    def get_arg(self):
        return self.arg
