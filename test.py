import networkx as nx
import matplotlib.pyplot as plt
import pydot
import pulp

G = nx.DiGraph()  # Directed graph

G.add_edge('s', 'u', weight=10, label='w 10')
G.add_edge('s', 'x', weight=5, label='w 5')
G.add_edge('u', 'v', weight=1, label='w 1')
G.add_edge('u', 'x', weight=2, label='w 2')

G.add_edge('v', 'y', weight=4, label='w 4')
G.add_edge('x', 'u', weight=3, label='w 3')
G.add_edge('x', 'v', weight=9, label='w 9')

G.add_edge('x', 'y', weight=2, label='w 2')
G.add_edge('y', 's', weight=7, label='w 7')
G.add_edge('y', 'v', weight=6, label='w 6')


# weight='weight' parameter in the add_edge functions
p = nx.shortest_path(G, source='s', weight='weight')

for x in {'u', 'v', 'x', 'y'}:
    print("Shortest path to node {} -> {}".format(x, p[x]))

M = nx.MultiDiGraph(G)
# p['u'][len(p)-1]=p['u'][-1]
M.add_edge(p['y'][-1], p['u'][-2], color='red')

nx.drawing.nx_pydot.write_dot(M, 'sp.dot')
# neato -Tpng sp.dot -o sp.png
# dot .... BETTER TO USE DOT
# Modify the dotfile by ading [pos="5,1!"] to modify the position of the node in the plotself.

prob = LpProblem("shortest path", LpMinimize)
edge = LpVariable.dicts("edge", G.edges(), lowBound=0, cat="Continuous")


def obj():
    dist = lpSum(edge[(org, dest)] * data["weight"]
                 for (org, dest, data) in (G.edges(data=True)))
    return dist


def constraints():
    constraints = []
    for x in G.nodes():
        inout_sum = lpSum(edge[(x, nto)] for nto in G.sucessors(x) - lpSum(edge[(nfrom, x)] for nfrom in G.predecessors(x))
                          if x == 's':
                              c=inout_sum == 1
                          elif x == 'v':
                              c=inout_sum == -1
                          else:
                              c=inout_sum == 0
                          constraints.append(c))
prob +=objective()
for c in constraints():
    prob+=c
prob.solve()
print(LpStatus[prob,status])

for org,dest in G.edges():
    v=value(edge[(org,dest)])
    if v>0:
        print(org,dest,v)
        M.add_edge(org,dest,color='blue')

print(value(prob.objective))

"""
nx.draw(G, with_labels = True)
plt.show()
plt.close()
nx.draw(M,with_labels=True)
plt.show()
"""
