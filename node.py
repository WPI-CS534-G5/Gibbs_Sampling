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

    def AddParernt(self, Node):
        self.parents.append(Node)

    def AddChild(self, Node):
        self.children.append(Node)

    def GetParents(self):
        return self.parents

    def GetChildren(self):
        return self.children

    def SetStatus(self, Status):
        self.status = Status

    def GetStatus(self):
        return self.status

    def CalculateProbability(self, Constraints):
        conditions = 1
        for cons in Constraints:
            conditions = conditions * options.get(cons)
        return probabilities.get(conditions)

    def GetMarkovBlanket(self):
        return self.markovBlanket

    def SetMarkovBlanket(self):
        self.markovBlanket.extend(self.parents)  # Adds all the parents to the Markov Blanket
        self.markovBlanket.extend(self.children)  # Adds all the children to the Markov Blanket
        for child in self.children:  # Loops through all the children
            for parent in child.parents:  # Loops through all the parents of each child
                if parent not in self.markovBlanket and parent != self:  # If any of those parents are not the Markov Blanket
                    self.markovBlanket.append(parent)  # It adds them to it
