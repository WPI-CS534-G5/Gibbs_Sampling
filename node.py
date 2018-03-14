class Node(object):
    """Node object in graph"""
    def __init__(self, name, table, probabilities, parents=[], children=[]):
        super(Node, self).__init__()
        self.children = children
        self.parents = parents

        self.name = name
        self.table = table
        self.probabilities = probabilities
         
        self.markov_blanket = []
    
    def add_child(self, child):
        return 

    def add_parent(self, parent):
        return

    def calculate_probability(self):
        return

    def get_markov_blanket(self):
        return
