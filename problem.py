"""
Problem 4
Developed by Carlos Sánchez Páez
Network Planning
Academic year 2018/19

"""

from tools import *  # File with all the necessary functions

DEBUG = False

# First, create the graph

G = create_graph()

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

# Finally, let's show the status of the problem, the final values for the variables and the cost.

print_problem(prob)

draw_graph(G)

# Draw the flow in the graph
# TODO!!!
