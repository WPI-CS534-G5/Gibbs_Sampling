
import settings
from prob import options, probabilities
from random import randint, randrange


query, iterations, evidence = settings.get_input()  # get command line input
Network = settings = settings.init_network()  # initialize network

# First set the evidence nodes
evidence_str = ''.join(evidence)
for node in Network:
    for condition in evidence:
        if condition.find(node.GetName()) != -1:
            node.SetStatus(condition)

# Find the queried node
qNode = None
for node in Network:
    if query == node.GetName():
        qNode = node
        break

Stats = []
for key in options:
    if qNode.GetName() in key:
        Stats.append(0)


# Function for initializing nodes that are not evidence nodes
def InitializeNodes(Network, cost_conditions):
    for node in Network:
        if node.GetName() not in cost_conditions:
            node.SetStatus(None)


# Function for randomly assinging probabilities to the nodes that are not evidence nodes
def RandomizeNodes(Network, cost_conditions):
    for node in Network:
        if node.GetName() not in cost_conditions:
            cnt = 0
            conds = []
            for key in options:
                if node.GetName() in key:
                    conds.append(key)
            node.SetStatus(conds[randint(0, len(conds)-1)])


# Iterate for as much as input
for iteration in range(0, iterations):

    # Second randomly assign other nodes
    RandomizeNodes(Network, evidence)

    # Iterate through the nodes of the Markov Blanket of the queried node
    for node in qNode.GetMarkovBlanket():

        Pn = []  # List of probabilities
        a = None  # Normalizing factor
        Result = []  # Resulting probabilities

        cnt = 0  # Number of types of predictors
        conds = []  # List of types of predictors

        # Get conditionals of node
        for key in options:
            if node.GetName() in key:
                cnt += 1
                conds.append(key)

        # Loop through node's conditions
        for cond in conds:
            # For Nodes Parents
            SubConstraints = list()
            SubConstraints.append(cond)
            for parent in node.GetParents():
                SubConstraints.append(parent.status)
            CondProb = node.CalculateProbability(SubConstraints)

            # For Nodes Children and Children's Parents
            print node.GetName()
            for child in node.GetChildren():
                SubConstraints = list()
                SubConstraints.append(cond)
                SubConstraints.append(child.GetStatus())
                for parent in child.GetParents():
                    if parent.GetName() not in cond:
                        SubConstraints.append(parent.GetStatus())

                CondProb = CondProb * node.CalculateProbability(SubConstraints)
            Result.append(CondProb)

        # Calculate the Normalizing factor
        Sum = sum(Result)
        a = 1 / Sum

        # Normalize the probabilities
        for pr in Result:
            pr = pr * a

        NormResult = []
        for i in range(0, len(Result) - 1):
            if len(NormResult) < 1:
                NormResult.append(Result[0])
            NormResult.append(Result[i] + NormResult[i - 1])

        RandNum = float(randrange(0, 1000)) / 1000

        FinalResult = None

        for i in range(0, len(NormResult)):
            if RandNum <= NormResult[i]:
                FinalResult = conds[i]

        qNode.SetStatus(FinalResult)

    # ############ End of qNode Markov Blanket

    for key in options:
        if qNode.GetName() in key:
            cnt = cnt + 1
            conds.append(key)

    Conds2 = []
    for i in range(0, cnt):
        for parent in qNode.GetParents():
            Conds2.append(parent.Status)
        Conds2.append(conds[i])
        Stats[i] = Stats[i] + qNode.CalculateProbability(conds)

for stat in Stats:
    stat = stat / iterations

# Calculate the Normalizing factor
Sum = None
for stat in Stats:
    Sum = Sum + stat
a = 1 / Sum

# Normalize the probabilities
for stat in Stats:
    stat = stat * a

for i in range(0, cnt):
    print('P(' + conds[i] + ') = ' + Stats[i])

