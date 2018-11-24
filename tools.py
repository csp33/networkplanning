"""
Problem 4
Developed by Carlos Sánchez Páez
Network Planning
Academic year 2018/19

"""

import networkx as nx
import matplotlib.pyplot as plt
import pydot
from pulp import *


def create_graph():
    G = nx.DiGraph()

    # Add the nodes
    G.add_node('A', pos=(0, 2))
    G.add_node('B', pos=(2, 3))
    G.add_node('C', pos=(2, 1))
    G.add_node('D', pos=(3.5, 2))
    G.add_node('E', pos=(5, 3))
    G.add_node('F', pos=(5, 1))
    G.add_node('G', pos=(7, 2))

    # Add the edges
    G.add_edge('A', 'B', cost=20, capacity=20)
    G.add_edge('A', 'C', cost=7, capacity=15)
    G.add_edge('B', 'E', cost=16, capacity=21)
    G.add_edge('B', 'D', cost=4, capacity=4)
    G.add_edge('C', 'D', cost=4, capacity=4)
    G.add_edge('C', 'F', cost=3, capacity=9)
    G.add_edge('D', 'E', cost=2, capacity=2)
    G.add_edge('D', 'F', cost=6, capacity=10)
    G.add_edge('E', 'G', cost=18, capacity=24)
    G.add_edge('F', 'G', cost=9, capacity=10)

    return G


def get_color_map(G):
    color_map = []

    for node in G:
        if node in {'G', 'A'}:  # Source and sink nodes
            color_map.append('red')
        else:
            color_map.append('blue')
    return color_map


def draw_graph(G):
    color_map = get_color_map(G)
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, node_color=color_map, with_labels=True, pos=pos)
    edge_labels = dict([((u, v,), "({},{})".format(
        d['cost'], d['capacity']))for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

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


def get_objective(G, variables):
    return lpSum(variables["{}-{}".format(edge[0], edge[1])] * G[edge[0]][edge[1]]['cost'] for edge in G.edges())


def print_problem(prob):
    print("Status:{}".format(LpStatus[prob.status]))

    for x in prob.variables():
        print("{}={}".format(x.name, x.varValue))

    print("The minimum cost is {}".format(value(prob.objective)))
