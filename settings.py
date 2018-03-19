import sys
from node import Node


# Example Query: $gibbs price schools=good location=ugly -u 10000 -d 0
def get_input():
    args = sys.argv
    query = args[2]
    iterations = int(args[-3])
    cost_conditions = []
    for arg in args:
        if not ("=" not in arg):
            cost_conditions.append(arg)

    return query, iterations, cost_conditions


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
    location.AddParernt(amenities)
    location.AddParernt(neighborhood)
    children.AddParernt(neighborhood)
    schools.AddParernt(children)
    price.AddParernt(schools)
    price.AddParernt(size)
    price.AddParernt(location)
    price.AddParernt(age)
    age.AddParernt(location)
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
