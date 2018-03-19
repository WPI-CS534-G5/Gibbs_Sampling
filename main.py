# main.py
from prob import options, probabilities
from node import Node
import sys
from random import randint



#Reading input
args = sys.argv
query = args[2]
iterations = args[-3]
cost_conditions = []
for arg in args:
    if(not("=" not in arg)):
        cost_conditions.append(arg)

#Define the Network
Network=[]
#Define the nodes and add the to the Network
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
Network.append(amenities)
Network.append(neighborhood)
Network.append(location)
Network.append(children)
Network.append(age)
Network.append(price)
Network.append(size)
Network.append(schools)


#First set the evidence nodes
for i in Network:
    for j in cost_conditions:
        if j.find(i.GetName()) != -1:
            i.SetStatus(j)

#Find the queried node
qNode = None
for node in Network:
    if query == node.GetName:
        qNode = node

Stats = []
for key in options:
    if qNode.GetName in key:
        Stats.append(0)

#Iterate for as much as inputed
for i in range(0, iterations):
    #Second randomly assign other nodes
    RandomizeNodes(Network,cost_conditions)

    #Iterate through the nodes of the Markov Blanket of the queried node
    for i in qNode.GetMarkovBlanket:

        Pn=[] # List of probabilities
        a = None # Normalizing factor
        Result=[] # Resulting probabilities

        cnt = 0 #Number of types of predictors
        conds=[] #List of types of predictors
        for key in options:
            if i.GetName in key:
                cnt = cnt +1
                conds.append(key)

        for cond in conds:
             SubConstraints=[]
             SubConstraints.append(cond)
             for parent in i.GetParents:
                 SubConstraints.append(parent.Status)
             CondProb = i.CalculateProbability(SubConstraints)

             for child in i.GetChildren:
                 SubConstraints=[]
                 SubConstraints.append(cond)
                 for parent in child.GetParents:
                     if parent.GetStatus not in cond:
                         SubConstraints.append(parent.GetStatus)
                 CondProb =CondProb* i.CalculateProbability(SubConstraints)
             Result.append(CondProb)


        # Calculate the Normalizing factor
        Sum = None
        for pr in Result:
            Sum = Sum + pr
        a = 1/Sum

        # Normalize the probabilities
        for pr in Result:
            pr = pr*a

        NormResult=[]

        for i in range(0, Result.size()-1):
            if NormResult.size()<1:
                NormResult.append(Result[0])
            NormResult.append(Result[i]+NormResult[i-1])


        RandNum = float(random.randrange(0, 1000))/1000

        FinalResult= None

        for i in range(0, NormResult.size()):
            if RandNum <= NormResult[i]:
                FinalResult= conds[i]

        qNode.SetStatus(FinalResult)

    ##End of qNode Markov Blanket

    for key in options:
        if qNode in key:
            cnt = cnt +1
            conds.append(key)

    Conds2 = []
    for i in range(0,cnt):
        for parent in qNode.GetParents:
            Conds2.append(parent.Status)
        Conds2.append(conds[i])
        Stats[i]= Stats[i]+ qNode.CalculateProbability(conds)


for stat in Stats:
    stat = stat/iterations

# Calculate the Normalizing factor
Sum = None
for stat in Stats:
    Sum = Sum + stat
a = 1/Sum

# Normalize the probabilities
for stat in Stats:
    stat = stat*a

for i in range(0,cnt):
    print('P('+conds[i]+') = ' + Stats[i])



#Function for randomly assinging probabilities to the nodes that are not evidence nodes
def RandomizeNodes(Network,cost_conditions):
    for node in Network:
        if node.GetName not in cost_conditions:
            cnt = 0
            conds=[]
            for key in options:
                if node.GetName in key:
                    cnt = cnt +1
                    conds.append(key)
            node.SetStatus(conds[randint(0, cnt-1)])

#Function for initializing nodes that are not evidence nodes
def InitializeNodes(Network,cost_conditions):
    for node in Network:
        if node.GetName not in cost_conditions:
            node.SetStatus(None)
