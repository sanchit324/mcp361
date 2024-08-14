import numpy as np

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
    # Get user inputs
    num_periods = int(input("Enter the number of periods: "))
    demand = list(map(int, input(f"Enter the demand for each period separated by spaces (total {num_periods} periods): ").split()))
    setup_cost = float(input("Enter the setup cost: "))
    holding_cost = float(input("Enter the holding cost: "))
    
    # Validate input lengths
    if len(demand) != num_periods:
        raise ValueError("The number of demand entries does not match the number of periods.")
    
    # Create an instance of WagnerWhitin with user inputs
    model = WagnerWhitin(demand, setup_cost, holding_cost)
    
    # Compute the optimal schedule
    model.compute_optimal_schedule()
    
    # Print the results
    model.print_table()
    
    # Get and print production schedule
    schedule = model.get_production_schedule()
    print("\nProduction Schedule:")
    for t, q in enumerate(schedule, 1):
        if q > 0:
            print(f"Produce {q} units at t = {t}")

if __name__ == "__main__":
    main()
