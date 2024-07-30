import pulp

# Parameters
profit = [12, 10, 7]  # Profit per product
demand = [700, 900, 450]  # Maximum demand for each product
lead = [21, 17, 14]  # Lead time for each product
capacity = [550, 750, 225]  # Capacity of each facility
max_lead = [10000, 7000, 4200]  # Maximum total lead time for each facility

# Create the model
model = pulp.LpProblem("Production_Allocation", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", [(i, j) for i in range(3) for j in range(3)], lowBound=0, cat='Integer')

# Objective function
model += pulp.lpSum(profit[i] * x[(i, j)] for i in range(3) for j in range(3))

# Constraints
# Demand constraint: Total production assigned to each product should not exceed its demand
for i in range(3):
    model += pulp.lpSum(x[(i, j)] for j in range(3)) <= demand[i]

# Capacity constraint: Total production at each facility should not exceed its capacity
for j in range(3):
    model += pulp.lpSum(x[(i, j)] for i in range(3)) <= capacity[j]

# Lead time constraint: Total lead time for production at each facility should not exceed the maximum allowed lead time
for j in range(3):
    model += pulp.lpSum(lead[i] * x[(i, j)] for i in range(3)) <= max_lead[j]

# Total batteries that can be produced in the factories
total_batteries = pulp.lpSum(x[(i, j)] for i in range(3) for j in range(3))

# Constraint: The Economy batteries must be 40% of total batteries
model += pulp.lpSum(x[(2, j)] for j in range(3)) >= 0.4 * total_batteries


# Solve
model.solve()

# Output: The output is generated in the allocation matrix
# Optimal Cost: is the objective function value of the model
allocation = [[x[(i, j)].varValue for j in range(3)] for i in range(3)]
optimal_profit = pulp.value(model.objective)

print("Optimal Allocation Matrix with Economy Constraint:")
for row in allocation:
    print(row)
print(f"Optimal Profit: {optimal_profit}")
