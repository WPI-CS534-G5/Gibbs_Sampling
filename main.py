# main.py
from prob import options, probabilities
import node
import sys
from random import randint

args = sys.argv

query = args[2]
iterations = args[-3]


cost_conditions = []

for arg in args:
    if(not("=" not in arg)):
        cost_conditions.append(arg)






# print(randint(0, 9))
