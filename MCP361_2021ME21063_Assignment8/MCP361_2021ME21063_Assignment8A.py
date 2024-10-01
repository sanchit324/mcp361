class TreeNode:
    def __init__(self, id, player, children, payoff):
        self.id = id  # Unique identifier for the node
        self.player = player  # Player making the decision at this node
        self.children = children  # List of child nodes [left_child, right_child]
        self.payoff = payoff  # Payoff vector for terminal nodes

def load_tree_from_file(filepath):
    tree = {}
    with open(filepath, 'r') as file:
        for line in file:
            data = line.strip().split()  # Split the line into components
            node_id = int(data[0])  # Node ID
            player = int(data[1]) if int(data[1]) != -1 else None  # Player number (or None if no player)
            children = [int(c) if int(c) != -1 else None for c in data[2:4]]  # Child node IDs
            payoff = eval(data[4]) if data[4] != '[]' else []  # Evaluate payoff as a list
            tree[node_id] = TreeNode(node_id, player, children, payoff)  # Create and store the node
    return tree  # Return the constructed game tree

def backward_induction_algorithm(tree):
    optimal_strategy = {}  # Dictionary to store optimal moves for each node

    def recursive_evaluation(node_id):
        node = tree[node_id]  # Get the current node
        if node.payoff:  # Check if it's a terminal node
            return node.payoff  # Return the payoff for terminal nodes
        else:
            # Recursively get the payoffs from the child nodes
            left_payoff = recursive_evaluation(node.children[0])  # Payoff from left child
            right_payoff = recursive_evaluation(node.children[1])  # Payoff from right child
            
            # Decision logic based on the current player's strategy
            if node.player == 1:  # Player 1 maximizes the first element of the payoff
                if left_payoff[0] >= right_payoff[0]:
                    optimal_strategy[node.id] = node.children[0]  # Select left child
                    node.payoff = left_payoff  # Update current node's payoff
                else:
                    optimal_strategy[node.id] = node.children[1]  # Select right child
                    node.payoff = right_payoff  # Update current node's payoff
            else:  # For Player 2 and subsequent players
                if left_payoff[1] >= right_payoff[1]:  # Compare second payoff
                    optimal_strategy[node.id] = node.children[0]  # Select left child
                    node.payoff = left_payoff  # Update current node's payoff
                else:
                    optimal_strategy[node.id] = node.children[1]  # Select right child
                    node.payoff = right_payoff  # Update current node's payoff

            return node.payoff  # Return the updated payoff for this node

    recursive_evaluation(0)  # Start evaluation from the root node
    return optimal_strategy  # Return the computed strategy

def print_results(strategy, tree):
    current_node = 0  # Start from the root node
    print("The determined strategy is as follows:")
    while current_node in strategy:  # Traverse the strategy path
        next_node = strategy[current_node]  # Get the next node from the strategy
        player = tree[current_node].player  # Get the current player
        print(f"At node {current_node}, Player {player} selects node {next_node}")
        current_node = next_node  # Move to the next node

    print(f"The strategy concludes at node {current_node}")  # Print final terminal node
    print(f"The resulting optimal payoff vector is {tree[current_node].payoff}\n" + "-" * 50)  # Print final payoff details

def main():
    # List of files containing game tree data
    input_files = [
        "MCP361_2021ME21063_Assignment8_Problem1.txt",
        "MCP361_2021ME21063_Assignment8_Problem2.txt",
        "MCP361_2021ME21063_Assignment8_Problem3.txt"
    ]
    
    for filepath in input_files:
        game_tree = load_tree_from_file(filepath)  # Load the game tree from the file
        strategy = backward_induction_algorithm(game_tree)  # Calculate optimal strategy
        print_results(strategy, game_tree)  # Print the strategy and optimal payoff

if __name__ == "__main__":
    main()  # Execute the main function
