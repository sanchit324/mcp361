# Importing the pulp library 
import pulp

# Costs matrix given in the question
costs = [
    [40, 45, 43, 60, 58],
    [44, 56, 48, 45, 48],
    [52, 39, 45, 51, 41],
    [40, 61, 49, 72, 45],
    [55, 45, 46, 52, 43]
]

# The model is created using pulp LpProblem module and since it is a minimisation problem we use LpMinimize
model = pulp.LpProblem("Assignment_Problem", pulp.LpMinimize)

# There are (n*n) decision variables for the problem and all of them are binary either 0 or 1. So, the variables are initialized
x = pulp.LpVariable.dicts("x", [(i, j) for i in range(5) for j in range(5)], 0, 1, pulp.LpBinary)

# Objective Function: The cost matrix is multiplied with the decision variables to generate an objective function
model += pulp.lpSum(costs[i][j] * x[(i, j)] for i in range(5) for j in range(5))

# Constraints
# Constraint1: A single person can perform only one task
# Constraint2: Each task needs only one person
for i in range(5):
    model += pulp.lpSum(x[(i, j)] for j in range(5)) == 1
for j in range(5):
    model += pulp.lpSum(x[(i, j)] for i in range(5)) == 1

# Solve
model.solve()

# Output: The output is generated in the allocation matrix
# Optimal Cost: is the objective function value of the model
if pulp.LpStatus[model.status] == 'Optimal':
    allocation = [[x[(i, j)].varValue for j in range(5)] for i in range(5)]
    optimal_cost = pulp.value(model.objective)
    print("Allocation Matrix:", allocation)
    print("Optimal Cost:", optimal_cost)
else:
    print("No optimal solution found. Status:", pulp.LpStatus[model.status])
