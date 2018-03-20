from prob import options, probabilities


class Node:
    def __init__(self, name):
        self.name = name
        self.parents = []
        self.children = []
        self.status = None
        self.markovBlanket = []

    def GetName(self):
        return self.name

    def AddParent(self, node):
        self.parents.append(node)

    def AddChild(self, node):
        self.children.append(node)

    def GetParents(self):
        return self.parents

    def GetChildren(self):
        return self.children

    def SetStatus(self, status):
        self.status = status

    def GetStatus(self):
        return self.status

    def GetMarkovBlanket(self):
        return self.markovBlanket

    def SetMarkovBlanket(self):
        self.markovBlanket.extend(self.parents)  # Adds all the parents to the Markov Blanket
        self.markovBlanket.extend(self.children)  # Adds all the children to the Markov Blanket
        for child in self.children:  # Loops through all the children
            for parent in child.parents:  # Loops through all the parents of each child
                if parent not in self.markovBlanket and parent != self:  # If any of those parents are not the Markov Blanket
                    self.markovBlanket.append(parent)  # It adds them to it


def CalculateProbability(constraints):
    conditions = 1
    for cons in constraints:
        conditions *= options.get(cons)
    return probabilities.get(conditions)
