import networkx as nx
import matplotlib.pyplot as plt

class TreeNode:
    def __init__(self, node_id, player, children, payoff):
        self.node_id = node_id  # Unique identifier for the node
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
            payoff = eval(data[4]) if data[4] != '[]' else [0, 0]  # Evaluate payoff as a list or default
            tree[node_id] = TreeNode(node_id, player, children, payoff)  # Create and store the node
    return tree  # Return the constructed game tree

def backward_induction_algorithm(tree):
    optimal_strategy = {}  # Dictionary to store optimal moves for each node

    def recursive_evaluation(node_id):
        node = tree[node_id]  # Get the current node
        if node.payoff != [0, 0]:  # Check if it's a terminal node (non-terminal nodes should have initial payoffs as [0,0])
            return node.payoff  # Return the payoff for terminal nodes
        else:
            # Recursively get the payoffs from the child nodes
            left_payoff = recursive_evaluation(node.children[0])  # Payoff from left child
            right_payoff = recursive_evaluation(node.children[1])  # Payoff from right child
            
            # Decision logic based on the current player's strategy
            if node.player == 1:  # Player 1 maximizes the first element of the payoff
                if left_payoff[0] >= right_payoff[0]:
                    optimal_strategy[node.node_id] = node.children[0]  # Select left child
                    node.payoff = left_payoff  # Update current node's payoff
                else:
                    optimal_strategy[node.node_id] = node.children[1]  # Select right child
                    node.payoff = right_payoff  # Update current node's payoff
            else:  # For Player 2 and subsequent players
                if left_payoff[1] >= right_payoff[1]:  # Compare second payoff
                    optimal_strategy[node.node_id] = node.children[0]  # Select left child
                    node.payoff = left_payoff  # Update current node's payoff
                else:
                    optimal_strategy[node.node_id] = node.children[1]  # Select right child
                    node.payoff = right_payoff  # Update current node's payoff

            return node.payoff  # Return the updated payoff for this node

    recursive_evaluation(0)  # Start evaluation from the root node
    return optimal_strategy  # Return the computed strategy

def draw_tree(tree, strategy):
    graph = nx.Graph()
    node_count = len(tree)
    graph.add_nodes_from(range(node_count))  # Add nodes to the graph

    edges = []
    for i in range(node_count):
        if tree[i].children[0] is not None:
            edges.append((i, tree[i].children[0]))  # Add edge to left child
        if tree[i].children[1] is not None:
            edges.append((i, tree[i].children[1]))  # Add edge to right child
    graph.add_edges_from(edges)  # Add edges to the graph

    # Define positions for the nodes to create a tree structure
    pos = {}
    def position_nodes(node_id, x, y, layer):
        pos[node_id] = (x, y)  # Assign position to the node
        if tree[node_id].children[0] is not None:
            position_nodes(tree[node_id].children[0], x - 1 / (layer + 1), y - 1, layer + 1)  # Left child
        if tree[node_id].children[1] is not None:
            position_nodes(tree[node_id].children[1], x + 1 / (layer + 1), y - 1, layer + 1)  # Right child

    position_nodes(0, 0, 0, 1)  # Start positioning from the root node

    plt.figure(figsize=(12, 8))
    
    # Draw the nodes
    nx.draw(graph, pos, with_labels=True, node_shape='s', node_color='lightblue', font_size=10, font_weight='bold')

    # Draw edges
    edge_labels = {}
    for i in range(node_count):
        if tree[i].player is not None:
            if tree[i].children[0] is not None:
                edge_labels[(i, tree[i].children[0])] = f"Player {tree[i].player}"
            if tree[i].children[1] is not None:
                edge_labels[(i, tree[i].children[1])] = f"Player {tree[i].player}"

    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    # Add payoffs to the nodes
    node_labels = {i: f"\nPayoff: {tuple(tree[i].payoff)}" for i in range(node_count)}
    for i in range(node_count):
        plt.text(pos[i][0], pos[i][1], f"{node_labels[i]}", fontsize=10, ha='center', va='center', color='black')

    plt.title("Game Tree Visualization")
    plt.axis('off')  # Turn off the axis
    plt.show()

def main():
    input_file = "MCP361_2021ME21063_Assignment8_Problem1.txt"
    game_tree = load_tree_from_file(input_file)  # Load the game tree from the file
    strategy = backward_induction_algorithm(game_tree)  # Calculate optimal strategy
    draw_tree(game_tree, strategy)  # Visualize the game tree

if __name__ == "__main__":
    main()  # Execute the main function
