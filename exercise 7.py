from pulp import *
import networkx as nx
import matplotlib.pyplot as plt


exercise = LpProblem("MCFP", LpMinimize)

x_1_a_c = LpVariable("x_1_a_c", lowBound=0, upBound=1, cat='Integer')
x_1_a_d = LpVariable("x_1_a_d", lowBound=0, upBound=1, cat='Integer')
x_1_c_f = LpVariable("x_1_c_f", lowBound=0, upBound=1, cat='Integer')
x_1_c_e = LpVariable("x_1_c_e", lowBound=0, upBound=1, cat='Integer')
x_1_e_g = LpVariable("x_1_e_g", lowBound=0, upBound=1, cat='Integer')
x_1_g_f = LpVariable("x_1_g_f", lowBound=0, upBound=1, cat='Integer')
x_1_d_f = LpVariable("x_1_d_f", lowBound=0, upBound=1, cat='Integer')
x_1_d_e = LpVariable("x_1_d_e", lowBound=0, upBound=1, cat='Integer')
x_1_d_c = LpVariable("x_1_d_c", lowBound=0, upBound=1, cat='Integer')
x_1_b_c = LpVariable("x_1_b_c", lowBound=0, upBound=1, cat='Integer')
x_1_b_d = LpVariable("x_1_b_d", lowBound=0, upBound=1, cat='Integer')


x_2_a_c = LpVariable("x_2_a_c", lowBound=0, upBound=1, cat='Integer')
x_2_a_d = LpVariable("x_2_a_d", lowBound=0, upBound=1, cat='Integer')
x_2_c_f = LpVariable("x_2_c_f", lowBound=0, upBound=1, cat='Integer')
x_2_c_e = LpVariable("x_2_c_e", lowBound=0, upBound=1, cat='Integer')
x_2_e_g = LpVariable("x_2_e_g", lowBound=0, upBound=1, cat='Integer')
x_2_g_f = LpVariable("x_2_g_f", lowBound=0, upBound=1, cat='Integer')
x_2_d_f = LpVariable("x_2_d_f", lowBound=0, upBound=1, cat='Integer')
x_2_d_e = LpVariable("x_2_d_e", lowBound=0, upBound=1, cat='Integer')
x_2_d_c = LpVariable("x_2_d_c", lowBound=0, upBound=1, cat='Integer')
x_2_b_c = LpVariable("x_2_b_c", lowBound=0, upBound=1, cat='Integer')
x_2_b_d = LpVariable("x_2_b_d", lowBound=0, upBound=1, cat='Integer')


# objective

exercise += 50 * x_1_a_c + 25 * x_1_a_d + 35 * x_1_b_c + 25 * x_1_b_d + 15 * x_1_c_e + 15 * x_1_c_f + 5 * x_1_d_c + 40 * x_1_d_f + 25 * x_1_d_e + 5 * \
    x_1_e_g + + 10 * x_1_g_f + 40 * x_2_a_c + 20 * x_2_a_d + 28 * x_2_b_c + 20 * x_2_b_d + 12 * \
    x_2_c_e + 12 * x_2_c_f + 4 * x_2_d_c + 32 * \
    x_2_d_f + 20 * x_2_d_e + 4 * x_2_e_g + 8 * x_2_g_f


# constraints

exercise += x_1_a_c + x_1_a_d == 1
exercise += x_1_b_c + x_1_b_d == 0
exercise += - x_1_a_c - x_1_b_c - x_1_d_c + x_1_c_e + x_1_c_f == 0
exercise += - x_1_a_d - x_1_b_d + x_1_d_c + x_1_d_f + x_1_d_e == 0
exercise += - x_1_c_e - x_1_d_e + x_1_e_g == 0
exercise += - x_1_d_f - x_1_c_f - x_1_g_f == -1
exercise += - x_1_e_g + x_1_g_f == 0

exercise += x_2_a_c + x_2_a_d == 0
exercise += x_2_b_c + x_2_b_d == 1
exercise += - x_2_a_c - x_2_b_c - x_2_d_c + x_2_c_e + x_2_c_f == 0
exercise += - x_2_a_d - x_2_b_d + x_2_d_c + x_2_d_f + x_2_d_e == 0
exercise += - x_2_c_e - x_2_d_e + x_2_e_g == -1
exercise += - x_2_d_f - x_2_c_f - x_2_g_f == 0
exercise += - x_2_e_g + x_2_g_f == 0

# capacity constraints

exercise += 5 * x_1_a_c + 4 * x_2_a_c <= 15
exercise += 5 * x_1_a_d + 4 * x_2_a_d <= 4
exercise += 5 * x_1_b_c + 4 * x_2_b_c <= 8
exercise += 5 * x_1_b_d + 4 * x_2_b_d <= 10
exercise += 5 * x_1_c_e + 4 * x_2_c_e <= 17
exercise += 5 * x_1_c_f + 4 * x_2_c_f <= 4
exercise += 5 * x_1_d_c + 4 * x_2_d_c <= 4
exercise += 5 * x_1_d_f + 4 * x_2_d_f <= 8
exercise += 5 * x_1_d_e + 4 * x_2_d_e <= 6
exercise += 5 * x_1_e_g + 4 * x_2_e_g <= 14
exercise += 5 * x_1_g_f + 4 * x_2_g_f <= 5


print(exercise)

exercise.solve()

print("Status:", LpStatus[exercise.status])

for v in exercise.variables():
    if v.varValue == 1:
        print(v.name, "=", v.varValue)


# Graph

G=nx.DiGraph()

G.add_node('A',pos=(1,2))
G.add_node('B',pos=(1,1))
G.add_node('C',pos=(2,2))
G.add_node('D',pos=(2,1))
G.add_node('E',pos=(3,2))
G.add_node('F',pos=(3,1))
G.add_node('G',pos=(4,1.5))

G.add_edge('A','C',cost=10,capacity=15)
G.add_edge('A','D',cost=5,capacity=4)
G.add_edge('B','C',cost=7,capacity=8)
G.add_edge('B','D',cost=5,capacity=10)
G.add_edge('C','E',cost=3,capacity=17)
G.add_edge('C','F',cost=3,capacity=4)
G.add_edge('D','E',cost=5,capacity=6)
G.add_edge('D','F',cost=8,capacity=8)
G.add_edge('D','C',cost=1,capacity=4)
G.add_edge('E','G',cost=1,capacity=14)
G.add_edge('G','F',cost=2,capacity=5)

# Show graph
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, with_labels=True, pos=pos)
edge_labels = dict([((u, v,), "({},{})".format(
d['cost'], d['capacity']))for u, v, d in G.edges(data=True)])
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()
plt.close()
# Show solution

solution=nx.MultiDiGraph()

solution.add_node('A',pos=(1,2))
solution.add_node('B',pos=(1,1))
solution.add_node('C',pos=(2,2))
solution.add_node('D',pos=(2,1))
solution.add_node('E',pos=(3,2))
solution.add_node('F',pos=(3,1))
solution.add_node('G',pos=(4,1.5))

solution.add_edge('A','C',cost=10,capacity=15,color='r')
solution.add_edge('A','D',cost=5,capacity=4,color='')
solution.add_edge('B','C',cost=7,capacity=8,color='')
solution.add_edge('B','D',cost=5,capacity=10,color='b')
solution.add_edge('C','E',cost=3,capacity=17,color='g')
solution.add_edge('C','F',cost=3,capacity=4,color='')
solution.add_edge('D','E',cost=5,capacity=6,color='')
solution.add_edge('D','F',cost=8,capacity=8,color='')
solution.add_edge('D','C',cost=1,capacity=4,color='b')
solution.add_edge('E','G',cost=1,capacity=14,color='r')
solution.add_edge('G','F',cost=2,capacity=5,color='r')

pos = nx.get_node_attributes(G, 'pos')
edge_colors = []
edge_width = []
for e in solution.edges(data='color'):
    if e[2] == 'r':
        edge_colors.append('red')
        edge_width.append(2)
    elif e[2] == 'b':
        edge_colors.append('blue')
        edge_width.append(2)
    elif e[2] == 'g':
        edge_colors.append('green')
        edge_width.append(2)
    else:
        edge_colors.append('black')
        edge_width.append(1)

nx.draw(G, with_labels=True,
    pos=pos, edge_color=edge_colors,width=edge_width)
edge_labels = dict([((u, v,), "({},{})".format(
d['cost'], d['capacity']))for u, v, d in G.edges(data=True)])
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()
plt.close()
