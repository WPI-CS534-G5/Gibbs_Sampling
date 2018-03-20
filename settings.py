import sys
from node import Node


# Example Query: $gibbs price schools=good location=ugly -u 10000 -d 0
# Input: $python main.py <query node> [args] [options]
# Args: evidence nodes to set e.g. school=bad
# Options: required: -u #of iterations, -d #of iterations to discard
def get_input():
    """
    :rtype: string, int, int, list
    """

    args = sys.argv[2:]

    query = sys.argv[1]
    discards = 0
    iterations = 0
    const_conditions = []

    for i in range(len(args) - 1):
        arg = args[i]
        if '=' in arg:
            const_conditions.append(arg)
        elif '-d' in arg:
            discards = int(args[i+1])
        elif '-u' in arg:
            iterations = int(args[i+1])

    return query, discards, iterations, const_conditions


def init_network():
    network = list()

    # Define the nodes and add the to the Network
    amenities = Node('amenities')
    neighborhood = Node('neighborhood')
    location = Node('location')
    children = Node('children')
    age = Node('age')
    price = Node('price')
    size = Node('size')
    schools = Node('schools')
    location.AddParent(amenities)
    location.AddParent(neighborhood)
    children.AddParent(neighborhood)
    schools.AddParent(children)
    price.AddParent(schools)
    price.AddParent(size)
    price.AddParent(location)
    price.AddParent(age)
    age.AddParent(location)
    amenities.AddChild(location)
    neighborhood.AddChild(location)
    neighborhood.AddChild(children)
    children.AddChild(schools)
    schools.AddChild(price)
    size.AddChild(price)
    location.AddChild(price)
    age.AddChild(price)
    location.AddChild(age)
    amenities.SetMarkovBlanket()
    neighborhood.SetMarkovBlanket()
    location.SetMarkovBlanket()
    children.SetMarkovBlanket()
    age.SetMarkovBlanket()
    price.SetMarkovBlanket()
    size.SetMarkovBlanket()
    schools.SetMarkovBlanket()
    network.append(amenities)
    network.append(neighborhood)
    network.append(location)
    network.append(children)
    network.append(age)
    network.append(price)
    network.append(size)
    network.append(schools)

    return network
