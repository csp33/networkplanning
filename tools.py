"""
Problem 4
Developed by Carlos Sánchez Páez
Network Planning
Academic year 2018/19

"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import pydot
from pulp import *


def create_graph():
    G = nx.DiGraph()

    # Add the nodes
    G.add_node('A', pos=(0, 2), demand=-10)  # Source node
    G.add_node('B', pos=(2, 3))
    G.add_node('C', pos=(2, 1))
    G.add_node('D', pos=(3.5, 2))
    G.add_node('E', pos=(5, 3))
    G.add_node('F', pos=(5, 1))
    G.add_node('G', pos=(7, 2), demand=10)  # Sink node

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
        if node == 'A':  # Source
            color_map.append('red')
        elif node == 'G':  # Sink
            color_map.append('green')
        else:
            color_map.append('blue')
    return color_map


def draw_graph(G):
    plt.figure(figsize=(8,6))
    color_map = get_color_map(G)
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, node_color=color_map, with_labels=True, pos=pos)
    edge_labels = dict([((u, v,), "({},{})".format(
        d['cost'], d['capacity']))for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.text(x=6, y=1, s='(cost,capacity)', fontsize='small')
    plt.text(x=-0.25, y=1, s='Flow value = 10', fontsize='small')
    legend_elements = [Line2D([0], [0], marker='o', color='w', label='Source',
                              markerfacecolor='r', markersize=15),
                       Line2D([0], [0], marker='o', color='w', label='Sink',
                              markerfacecolor='g', markersize=15)]
    plt.legend(handles=legend_elements, loc='upper right')
    plt.show()
    plt.close()


def draw_solution(G, d):
    plt.figure(figsize=(8,6))
    color_map = get_color_map(G)
    pos = nx.get_node_attributes(G, 'pos')
    edge_colors = []
    edge_width = []
    for key, value in d.items():
        for second_key, second_value in value.items():
            if second_value != 0:
                edge_colors.append('r')
                edge_width.append(2)
            else:
                edge_colors.append('b')
                edge_width.append(1)

    nx.draw(G, node_color=color_map, with_labels=True,
            pos=pos, edge_color=edge_colors, width=edge_width)
    edge_labels = dict([((u, v,), "({},{})".format(
        d['cost'], d['capacity']))for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.text(x=6, y=1, s='(cost,capacity)', fontsize='small')
    plt.text(x=-0.25, y=1, s='Flow value = 10', fontsize='small')
    legend_elements = [Line2D([0], [0], marker='o', color='w', label='Source',
                              markerfacecolor='r', markersize=15),
                       Line2D([0], [0], marker='o', color='w', label='Sink',
                              markerfacecolor='g', markersize=15),
                       Line2D([0], [0], marker='_', color='r', label='Minimum cost flow',
                              markerfacecolor='r', markersize=15)]
    plt.legend(handles=legend_elements, loc='upper right')
    plt.savefig('solution.png')
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


def print_solution(prob):
    print("Status:{}".format(LpStatus[prob.status]))

    for x in prob.variables():
        if x.varValue != 0:
            print("{}={}".format(x.name, x.varValue))

    print("The minimum cost is {}".format(value(prob.objective)))
