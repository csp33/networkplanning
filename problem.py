"""
Problem 4
Developed by Carlos Sánchez Páez
Network Planning
Academic year 2018/19

"""

from tools import *  # File with all the necessary functions

DEBUG = False
USE_PULP = True

# First, create the graph

G = create_graph()

print("Using PuLP to solve the problem? {}".format(USE_PULP))

if USE_PULP:
    # Method 1: calculate it using linear programming with PuLP

    # Then, we define the problem

    prob = LpProblem("Minimum Cost Flow", LpMinimize)

    # Create the variables

    variables = get_variables(G)

    # Add the constraints

    constraints = get_constraints(variables)

    for c in constraints:
        prob += c

    # Now, the objective function

    objective = get_objective(G, variables)

    prob += objective

    # Let's print the problem to verify that the input data is OK (debugging)
    if DEBUG:
        print(prob)

    # Save the problem to a file

    prob.writeLP("min_cost.lp")

    # Let's solve it!

    prob.solve()

    # Let's show the status of the problem, the final values for the variables and the cost.

    print_solution(prob)

    # Finally, let's create the dictionary to plot the solution graph

    flow_dict={}
    for node in G.nodes():
        flow_dict[node]={}

    for x in prob.variables():
        flow_dict[x.name[0]][x.name[2]]=x.varValue


else:
    # Method 2: calculate it using networkx_simplex method

    flow_cost, flow_dict = nx.network_simplex(G, weight='cost')

    print("The minimum cost is {}".format(flow_cost))
    for key, value in flow_dict.items():
        for second_key, second_value in value.items():
            if second_value != 0:
                print("{}-{}={}".format(key, second_key, second_value))


#draw_graph(G)
draw_solution(G,flow_dict)
