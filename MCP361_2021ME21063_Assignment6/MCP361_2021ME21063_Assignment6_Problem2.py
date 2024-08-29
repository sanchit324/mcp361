import numpy as np
import matplotlib.pyplot as plt

class EpsilonGreedyMAB:
    def __init__(self, num_arms, num_iterations, time_steps):
        # Initialize the Multi-Armed Bandit with epsilon-greedy strategy
        self.num_arms = num_arms  # Number of arms in the bandit
        self.num_iterations = num_iterations  # Number of iterations for the simulation
        self.time_steps = time_steps  # Number of time steps for the simulation
        
        # Generate true values for each arm across all iterations
        self.true_values = np.random.normal(0, 1, (num_iterations, num_arms))
        # Determine the optimal arm for each iteration
        self.optimal_arms = np.argmax(self.true_values, axis=1)
        
    def run_simulation(self, epsilon):
        # Initialize arrays for tracking arm pulls and estimated values
        arm_counts = np.zeros((self.num_iterations, self.num_arms))  # Initialize pull counts to zero
        estimated_values = np.zeros((self.num_iterations, self.num_arms))  # Initialize estimated values to zero
        
        average_rewards = []  # List to store average rewards over time
        optimal_action_percentage = []  # List to store percentage of optimal actions over time
        
        for step in range(self.time_steps):
            step_rewards = []  # List to store rewards for the current time step
            optimal_actions = 0  # Counter for the number of optimal actions
            
            for iteration in range(self.num_iterations):
                # Decide whether to explore or exploit based on epsilon
                if np.random.random() < epsilon:
                    # Explore: choose a random arm
                    chosen_arm = np.random.randint(self.num_arms)
                else:
                    # Exploit: choose the arm with the highest estimated value
                    chosen_arm = np.argmax(estimated_values[iteration])
                
                # Check if the chosen arm is the optimal arm
                if chosen_arm == self.optimal_arms[iteration]:
                    optimal_actions += 1  # Increment the count of optimal actions
                    
                # Generate a reward for the chosen arm
                reward = np.random.normal(self.true_values[iteration][chosen_arm], 1)
                step_rewards.append(reward)  # Store the reward
                
                # Update the counts and estimated values for the chosen arm
                arm_counts[iteration][chosen_arm] += 1
                estimated_values[iteration][chosen_arm] += (reward - estimated_values[iteration][chosen_arm]) / arm_counts[iteration][chosen_arm]
            
            # Compute and store the average reward for the current time step
            average_rewards.append(np.mean(step_rewards))
            # Compute and store the percentage of optimal actions for the current time step
            optimal_action_percentage.append(float(optimal_actions) / self.num_iterations * 100)
        
        return average_rewards, optimal_action_percentage
    
    def run_multiple_epsilons(self, epsilons):
        # Run simulations for multiple epsilon values
        results = {}  # Dictionary to store results for each epsilon
        for epsilon in epsilons:
            # Run simulation for the current epsilon
            avg_rewards, opt_action_pct = self.run_simulation(epsilon)
            # Store the results in the dictionary
            results[epsilon] = (avg_rewards, opt_action_pct)
        return results
    
    def plot_results(self, results):
        # Create subplots for average rewards and percentage of optimal actions
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        for epsilon, (avg_rewards, opt_action_pct) in results.items():
            # Plot average rewards for each epsilon
            ax1.plot(avg_rewards, label=f'ε = {epsilon}')
            # Plot percentage of optimal actions for each epsilon
            ax2.plot(opt_action_pct, label=f'ε = {epsilon}')
        
        # Set titles and labels for the plots
        ax1.set_title("Average Rewards for ε-Greedy")
        ax1.set_xlabel("Steps")
        ax1.set_ylabel("Average Reward")
        ax1.legend()  # Show legend for the plot
        
        ax2.set_title("Percentage of Optimal Actions for ε-Greedy")
        ax2.set_xlabel("Steps")
        ax2.set_ylabel("% Optimal Action")
        ax2.legend()  # Show legend for the plot
        
        # Adjust layout to prevent overlap and display the plots
        plt.tight_layout()
        plt.show()

# Parameters for the simulation
num_arms = 10  # Number of arms in the bandit
num_iterations = 1000  # Number of iterations
time_steps = 500  # Number of time steps
epsilons = [0, 0.01, 0.05, 0.1, 0.25]  # Different epsilon values to test

# Create an instance of the EpsilonGreedyMAB class
mab = EpsilonGreedyMAB(num_arms, num_iterations, time_steps)
# Run simulations for multiple epsilon values
results = mab.run_multiple_epsilons(epsilons)
# Plot the results
mab.plot_results(results)
