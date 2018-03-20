import settings
from prob import options
from random import randint, randrange
from node import Node, CalculateProbability

# ################################################# #
# ####### Initialize Network and Statistics ####### #
# ################################################# #

query, discards, iterations, evidence = settings.get_input()  # get command line input
network = settings = settings.init_network()  # initialize network

# First set the evidence nodes
for node in network:
    for condition in evidence:
        if condition.find(node.GetName()) is not -1:
            node.SetStatus(condition)

# Find the queried node
qNode = None  # type: Node
for node in network:
    if query == node.GetName():
        qNode = node
        break

# Find options to calculate probabilities for
stats = []
for key in options:
    if qNode.GetName() in key:
        stats.append(0)

# ########################################### #
# ####### Helper Function Definitions ####### #
# ########################################### #


# Update Nodes in Markov Blanket
def update_blanket(node):
    # Get conditionals of node
    conds = []
    for key in options:
        if node.GetName() in key:
            conds.append(key)

    # ####### Probability Calculations ####### #

    # Get Node's Conditional Probabilities
    result = conditional_probability(conds, node)

    # Calculate the Normalizing factor
    Sum = sum(result)
    a = 1 / Sum
    # Normalize the probabilities
    result = [prob * a for prob in result]

    # Calculate ranges for values conditions
    ranges = []
    for i in range(0, len(result) - 1):
        if len(ranges) < 1:
            ranges.append(result[0])
        else:
            ranges.append(result[i] + ranges[i - 1])

    # Calculate new condition for node
    new_condition = None
    rand_num = float(randrange(0, 1000)) / 1000

    for i in range(0, len(conds)-1):
        if rand_num <= ranges[i]:
            new_condition = conds[i]
    if not new_condition:
        new_condition = conds[-1]

    node.SetStatus(new_condition)


# Find conditional probability of node based on its Markov Blanket
def conditional_probability(conditions, node):
    probs = list()

    # Loop through node's conditions
    for cond in conditions:
        sub_condition_parents = list()
        sub_condition_parents.append(cond)

        # Loop through Node's Parents
        for parent in node.GetParents():
            sub_condition_parents.append(parent.status)
        conditional_prob = CalculateProbability(sub_condition_parents)

        # Loop through Node's Children
        for child in node.GetChildren():
            sub_condition_children = list()
            sub_condition_children.append(cond)
            sub_condition_children.append(child.GetStatus())

            # Loop through Children's Parents
            for parent in child.GetParents():
                if parent.GetName() not in cond:
                    sub_condition_children.append(parent.GetStatus())
            conditional_prob = conditional_prob * CalculateProbability(sub_condition_children)

        probs.append(conditional_prob)

    return probs


# Function for initializing nodes that are not evidence nodes
def initialize_nodes(net, cost_conditions):
    for n in net:
        if n.GetName() not in cost_conditions:
            n.SetStatus(None)


# Function for randomly assigning probabilities to the nodes that are not evidence nodes
def randomize_nodes(net, const_conditions):
    for n in net:
        if n.GetName() not in const_conditions:
            conditions = []
            for key in options:
                if n.GetName() in key:
                    conditions.append(key)
            n.SetStatus(conditions[randint(0, len(conditions)-1)])


# ################################# #
# ####### Begin Gibbs Logic ####### #
# ################################# #

qNode_conditions = []  # List of conditions
for key in options:
    if qNode.GetName() in key:
        qNode_conditions.append(key)


for iteration in range(1, iterations):
    randomize_nodes(network, evidence)  # Randomly assign other nodes

    # For each node in Markov Blanket of Queried Node
    for node in qNode.GetMarkovBlanket():
        update_blanket(node)

    # ####### End of qNode Markov Blanket ####### #

    # Calculate Probability of qNode
    print qNode_conditions
    exit(0)
    results = conditional_probability(qNode_conditions, qNode)
    for i in range(0, len(qNode_conditions)):
        stats[i] = stats[i] + results[i]


# ################################################# #
# ####### Final Step: Calculate Probability ####### #
# ################################################# #

# Divide by iterations
stats = [stat / iterations for stat in stats]

print stats

# Calculate the Normalizing factor
Sum = sum(stats)
a = 1 / Sum

# Normalize the probabilities
for stat in stats:
    stat = stat * a

for i in range(0, len(qNode_conditions)):
    print 'P(' + qNode_conditions[i] + ') = ' + str(stats[i])

