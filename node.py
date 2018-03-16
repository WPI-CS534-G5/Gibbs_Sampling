
class Node(object):
    def __init__(self, name, parents=None, children=None, status=None, probability=None, markov_blanket=None):
        super(Node, self).__init__()
        self.name = name
        self.parents = parents
        self.children = children

        self.status = status
        self.probability = probability
        self.markov_blanket = markov_blanket

    def add_parent(self, node):
        self.parents.append(node)

    def add_child(self, node):
        self.children.append(node)

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def calculate_probability(self):
        return

    def set_markov_blanket(self):
        self.markov_blanket.extend(self.parents)  # Adds all the parents to the Markov Blanket
        self.markov_blanket.extend(self.children)  # Adds all the children to the Markov Blanket

        for child in self.children:  # Loops through all the children
            for parent in child.parents:  # Loops through all the parents of each child
                if parent not in self.markov_blanket:  # If any of those parents are not the Markov Blanket
                    self.markov_blanket.append(parent)  # It adds them to it
