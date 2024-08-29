import numpy as np
import matplotlib.pyplot as plt

class MultiArmedBandit:
    def __init__(self, num_arms, num_iterations, time_steps):
        # Initialize the Multi-Armed Bandit problem
        self.num_arms = num_arms  # Number of arms in the bandit
        self.num_iterations = num_iterations  # Number of iterations for the simulation
        self.time_steps = time_steps  # Number of time steps for the simulation
        
        # Generate true values for each arm across all iterations
        self.true_values = np.random.normal(0, 1, (num_iterations, num_arms))
        # Determine the optimal arm for each iteration
        self.optimal_arms = np.argmax(self.true_values, axis=1)
        
    def run_simulation(self):
        # Initialize the counts and estimated values for each arm
        arm_counts = np.ones((self.num_iterations, self.num_arms))  # Each arm is initially pulled once
        estimated_values = np.zeros((self.num_iterations, self.num_arms))  # Start with zero estimates
        
        # Perform the initial pull for each arm to generate initial rewards
        rewards = np.random.normal(self.true_values, 1)
        # Store the mean of the initial rewards
        average_rewards = [np.mean(rewards)]
        # Initialize percentage of optimal actions
        optimal_action_percentage = [0]
        
        # Run the simulation for each time step
        for step in range(1, self.time_steps):
            step_rewards = []  # List to store rewards for the current time step
            optimal_actions = 0  # Counter for optimal actions
            
            # Iterate through each bandit problem
            for iteration in range(self.num_iterations):
                # Choose the arm with the highest estimated value
                chosen_arm = np.argmax(estimated_values[iteration])
                
                # Check if the chosen arm is the optimal one
                if chosen_arm == self.optimal_arms[iteration]:
                    optimal_actions += 1  # Increment the count of optimal actions
                    
                # Generate reward for the chosen arm
                reward = np.random.normal(self.true_values[iteration][chosen_arm], 1)
                step_rewards.append(reward)
                
                # Update counts and estimated values for the chosen arm
                arm_counts[iteration][chosen_arm] += 1
                estimated_values[iteration][chosen_arm] += (reward - estimated_values[iteration][chosen_arm]) / arm_counts[iteration][chosen_arm]
            
            # Append the average reward for the current time step
            average_rewards.append(np.mean(step_rewards))
            # Append the percentage of optimal actions for the current time step
            optimal_action_percentage.append(float(optimal_actions) / self.num_iterations * 100)
        
        return average_rewards, optimal_action_percentage
    
    def plot_results(self, average_rewards, optimal_action_percentage):
        # Create subplots for average rewards and percentage of optimal actions
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        
        # Plot average rewards
        ax1.plot(average_rewards)
        ax1.set_title("Average Rewards for Multi-Armed Bandit")
        ax1.set_xlabel("Steps")
        ax1.set_ylabel("Average Reward")
        
        # Plot percentage of optimal actions
        ax2.plot(optimal_action_percentage)
        ax2.set_title("Percentage of Optimal Actions")
        ax2.set_xlabel("Steps")
        ax2.set_ylabel("% Optimal Action")
        
        # Adjust layout to prevent overlap and show the plots
        plt.tight_layout()
        plt.show()

# Initialize and run the Multi-Armed Bandit simulation
bandit = MultiArmedBandit(num_arms=10, num_iterations=1000, time_steps=500)
avg_rewards, opt_action_pct = bandit.run_simulation()
bandit.plot_results(avg_rewards, opt_action_pct)
