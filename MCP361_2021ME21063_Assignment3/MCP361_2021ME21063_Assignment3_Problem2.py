import numpy as np

def calculate_setup_cost(setup_time, tool_wear_rate, tool_cost, oil_cost_per_liter, oil_required, operator_salary):
    """
    Calculate the total setup cost including tool wear, oil, and operator salary.
    """
    # Tool wear cost per setup
    tool_cost_per_setup = tool_wear_rate * setup_time * tool_cost
    # Operator cost per setup
    operator_cost_per_setup = setup_time * operator_salary
    # Total setup cost
    total_setup_cost = tool_cost_per_setup + (oil_required * oil_cost_per_liter) + operator_cost_per_setup
    return total_setup_cost

def calculate_holding_cost(warehouse_rent_per_sqft, warehouse_size, electricity_charges, maintenance_charges, units_stored):
    """
    Calculate the holding cost per unit including warehouse rent, electricity, and maintenance.
    """
    # Total monthly storage cost
    total_storage_cost = (warehouse_rent_per_sqft * warehouse_size) + electricity_charges + maintenance_charges
    # Holding cost per unit per month
    holding_cost_per_unit = total_storage_cost / units_stored
    return holding_cost_per_unit

class WagnerWhitin:
    def __init__(self, demand, setup_cost, holding_cost):
        """
        Initialize the Wagner-Whitin model with demand, setup cost, and holding cost.
        """
        self.demand = demand
        self.setup_cost = setup_cost
        self.holding_cost = holding_cost
        self.N = len(demand)  # Number of periods
        self.Z = np.zeros(self.N + 1)  # Array to store minimum costs
        self.j = np.zeros(self.N + 1, dtype=int)  # Array to store the last production period
        self.table = np.full((self.N, self.N), np.inf)  # Cost table initialized with infinity
    
    def compute_optimal_schedule(self):
        """
        Compute the optimal production schedule using the Wagner-Whitin algorithm.
        """
        for t in range(1, self.N + 1):  # Iterate over each period
            min_cost = float('inf')  # Initialize minimum cost as infinity
            for k in range(1, t + 1):  # Iterate over each possible production start
                # Calculate the cost of producing from period k to t
                cost = self.Z[k - 1] + self.setup_cost + self.holding_cost * sum((i - k) * self.demand[i - 1] for i in range(k, t + 1))
                self.table[k - 1, t - 1] = cost  # Store the cost in the table
                if cost < min_cost:  # Check if the current cost is the lowest
                    min_cost = cost  # Update minimum cost
                    self.j[t] = k  # Update the last production period for the current period
            self.Z[t] = min_cost  # Store the minimum cost for the current period
    
    def get_production_schedule(self):
        """
        Derive the production schedule from the computed last production period array.
        """
        schedule = [0] * self.N  # Initialize production schedule
        t = self.N  # Start from the last period
        while t > 0:  # Loop until all periods are covered
            k = self.j[t]  # Get the last production period
            schedule[k - 1] = sum(self.demand[k - 1:t])  # Calculate production for period k
            t = k - 1  # Move to the period before the last production period
        return schedule  # Return the production schedule
    
    def print_table(self):
        """
        Print the cost table, Z values, and j values in a formatted way.
        """
        """
        [INFO] Help is taken from ChatGPT for formatting the printing area
        """
        """
        The values are printed in integer format to take care of the formatting from previous question, if using float the table generated is not aligned properly.
        """
        print("Last week\t|\t Planning Horizon t")
        print("with Production\t|", end="")
        for t in range(1, len(self.Z)):  # Print headers for each period
            print(f"{t}\t", end="| ")
        print()
        print("-" * (12 + len(self.Z) * 9))  # Print separator
        
        for i in range(len(self.table)):  # Print each row of the cost table
            print(f"{i + 1}\t\t|", end="")
            for t in range(len(self.table[i])):
                if self.table[i, t] != np.inf:  # Check if the cost is not infinity
                    print(f"{self.table[i, t]:.0f}\t", end="| ")  # Print the cost
                else:
                    print("\t", end="| ")  # Print empty cell for infinity
            print()
            print("-" * (12 + len(self.Z) * 9))  # Print separator
        
        # Print Z values (minimum costs)
        print(f"Z*_t\t\t|", end="")
        for t in range(1, len(self.Z)):
            print(f"{self.Z[t]:.0f}\t", end="| ")
        print()
        print("-" * (12 + len(self.Z) * 9))
        
        # Print j values (last production periods)
        print(f"j*_t\t\t|", end="")
        for t in range(1, len(self.Z)):
            print(f"{self.j[t]}\t", end="| ")
        print()
        print("-" * (12 + len(self.Z) * 9))

def main():
    """
    Main function to handle user input, run the Wagner-Whitin model, and display results.
    """
    # Parameters for cost calculations
    setup_time = 75 / 60  # Time in hours
    tool_wear_rate = 0.005
    tool_cost = 2500
    oil_cost_per_liter = 100
    oil_required = 0.4
    operator_salary = 50
    warehouse_rent_per_sqft = 2
    warehouse_size = 500
    electricity_charges = 100
    maintenance_charges = 100
    units_stored = 500

    # Calculate setup and holding costs
    setup_cost = calculate_setup_cost(setup_time, tool_wear_rate, tool_cost, oil_cost_per_liter, oil_required, operator_salary)
    holding_cost = calculate_holding_cost(warehouse_rent_per_sqft, warehouse_size, electricity_charges, maintenance_charges, units_stored)
    
    print("Setup Cost: ", setup_cost)
    print("Holding Cost: ", holding_cost)

    # Input demand values
    demand = [100, 90, 115, 120, 95, 100, 90, 105, 105, 100, 110, 105]

    # Create an instance of WagnerWhitin
    model = WagnerWhitin(demand, setup_cost, holding_cost)
    
    # Compute the optimal schedule
    model.compute_optimal_schedule()
    
    # Print cost table and optimal values
    model.print_table()
    
    # Get and print production schedule
    schedule = model.get_production_schedule()
    print("\nProduction Schedule:")
    for t, q in enumerate(schedule, 1):
        if q > 0:
            print(f"Produce {q} units at t = {t}")

if __name__ == "__main__":
    main()
