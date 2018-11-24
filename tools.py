import networkx as nx
import matplotlib.pyplot as plt
import pydot
from pulp import *

def create_graph():
    G = nx.DiGraph()

    # Add the edges

    G.add_edge('A', 'B', cost=20, capacity=20, label='(20,20)', color='r')
    G.add_edge('A', 'C', cost=7, capacity=15, label='(7,15)', color='b')
    G.add_edge('B', 'E', cost=16, capacity=21, label='(16,21)', color='b')
    G.add_edge('B', 'D', cost=4, capacity=4, label='(4,4)', color='b')
    G.add_edge('C', 'D', cost=4, capacity=4, label='(4,4)', color='b')
    G.add_edge('C', 'F', cost=3, capacity=9, label='(3,9)', color='b')
    G.add_edge('D', 'E', cost=2, capacity=2, label='(2,2)', color='b')
    G.add_edge('D', 'F', cost=6, capacity=10, label='(6,10)', color='b')
    G.add_edge('E', 'G', cost=18, capacity=24, label='(18,24)', color='b')
    G.add_edge('F', 'G', cost=9, capacity=10, label='(9,10)', color='r')

    return G


def print_graph(G):
    color_map = []
    for node in G:
        if node in {'G', 'A'}:  # Source and sink nodes
            color_map.append('red')
        else:
            color_map.append('blue')

    nx.draw(G, node_color=color_map, with_labels=True)
    plt.show()
    plt.close()

def get_variables(G):
    variables = {}
    for edge in G.edges():
        name = '{}-{}'.format(edge[0], edge[1])
        upBound = G[edge[0]][edge[1]]['capacity']
        variables[name] = LpVariable(
            name, 0, G[edge[0]][edge[1]]['capacity'], cat='Integer')
    return variables

def get_constraints(variables):
    constraints = []
    constraints.append(variables['A-B'] +
                       variables['A-C'] <= 10)  # Source node
    constraints.append(variables['E-G'] + variables['F-G'] == 10)  # Sink node
    # Intermediate nodes
    constraints.append(variables['A-B'] -
                       variables['B-E'] - variables['B-D'] == 0)
    constraints.append(variables['A-C'] -
                       variables['C-D'] - variables['C-F'] == 0)
    constraints.append(
        variables['B-D'] + variables['C-D'] - variables['D-E'] - variables['D-F'] == 0)
    constraints.append(variables['B-E'] +
                       variables['D-E'] - variables['E-G'] == 0)
    constraints.append(variables['C-F'] +
                       variables['D-F'] - variables['F-G'] == 0)
    return constraints


def get_objective(G,variables):
    return lpSum(variables["{}-{}".format(edge[0], edge[1])] * G[edge[0]][edge[1]]['cost'] for edge in G.edges())

def print_problem(prob):
    print("Status:{}".format(LpStatus[prob.status]))

    for x in prob.variables():
        print("{}={}".format(x.name, x.varValue))

    print("The minimum cost is {}".format(value(prob.objective)))
