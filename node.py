

class Node:

    parents = []
    children = []
    status = None
    name = None
    markovBlanket = []

    def __init__(self,parents,children, status,table,name,probability,markovBlanket):
        super(Node, self).__init__()
        self.parents = parents
        self.children = children
        self.status = status
        self.table = table
        self.name = name
        self.markovBlanket = markovBlanket

    def AddParern(Node):
        self.parents.append(Node)

    def AddChild(Node):
        self.append(Node)

    def SetStatus(Status):
        self.status = Status

    def GetStatus():
        return self.status

    def CalculateProbability(Constraints):


        conditions = 1
        for cons in Constraints:
            conditions= conditions*options.get(cons)
        return probabilities.get(conditions)


    def SetMarkovBlanket():
        self.markovBlanket.extend(self.parents) # Adds all the parents to the Markov Blanket
        self.markovBlanket.extend(self.children) # Adds all the children to the Markov Blanket
        for child in children: # Loops through all the children
            for parent in child.parents: # Loops through all the parents of each child
                if parent not in self.markovBlanket: # If any of those parents are not the Markov Blanket
                    self.markovBlanket.append(parent) # It adds them to it
