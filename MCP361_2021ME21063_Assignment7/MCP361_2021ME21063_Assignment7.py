def load_game_data(file_path):
    # Open the file and read all lines
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    game_data = []
    # Process each line to extract game data
    for line in lines:
        rows = line.strip().split()
        # Convert each cell from string to a list of floats
        game_data.append([list(map(float, cell.split(','))) for cell in rows])
    
    return game_data

def determine_optimal_strategies(game_data, response_matrix):
    num_rows = len(game_data)  # Number of strategies for Player 1
    num_cols = len(game_data[0])  # Number of strategies for Player 2

    # Determine optimal strategies for Player 2
    for r in range(num_rows):
        # Find the maximum payoff for Player 2 in the current row
        max_payoff_player2 = max(cell[1] for cell in game_data[r])
        for c in range(num_cols):
            # If current cell has the maximum payoff for Player 2, mark it in the response matrix
            if game_data[r][c][1] == max_payoff_player2:
                response_matrix[r][c][1] = 1

    # Determine optimal strategies for Player 1
    for c in range(num_cols):
        # Find the maximum payoff for Player 1 in the current column
        max_payoff_player1 = max(game_data[r][c][0] for r in range(num_rows))
        for r in range(num_rows):
            # If current cell has the maximum payoff for Player 1, mark it in the response matrix
            if game_data[r][c][0] == max_payoff_player1:
                response_matrix[r][c][0] = 1

def find_and_display_nash_equilibria(game_data, response_matrix, file_path):
    rows, cols = len(game_data), len(game_data[0])  # Get dimensions of the game data
    print(f"\n{file_path}\n{'-'*45}")  # Indicate which file is being processed with a separator
    found_equilibrium = False  # Flag to track if any Nash Equilibrium is found
    
    # Iterate through all cells to find Nash Equilibria
    for r in range(rows):
        for c in range(cols):
            # Check if both players' strategies are optimal at this cell
            if response_matrix[r][c][0] == 1 and response_matrix[r][c][1] == 1:
                print(f"Player 1 chooses strategy {r+1} and Player 2 chooses strategy {c+1}")  # Output the equilibrium with clear formatting
                found_equilibrium = True
    
    # If no Nash Equilibrium was found, print a message
    if not found_equilibrium:
        print("No Nash Equilibrium identified.")
    print(f"{'-'*45}\n")  # End with a separator for clarity


def process_game_file(file_path):
    # Load the game data from the specified file
    game_data = load_game_data(file_path)
    rows, cols = len(game_data), len(game_data[0])  # Get the dimensions of the game data
    # Initialize a response matrix to track optimal strategies
    response_matrix = [[[0, 0] for _ in range(cols)] for _ in range(rows)]
    
    # Determine the optimal strategies for both players
    determine_optimal_strategies(game_data, response_matrix)
    
    # Find and display the Nash Equilibria based on the response matrix
    find_and_display_nash_equilibria(game_data, response_matrix, file_path)

def process_multiple_files(file_list):
    # Process each file in the provided list of game files
    for file in file_list:
        process_game_file(file)

def main():
    # List of game files to process
    game_file_list = [
        "MCP361_2021ME21063_Assignment7_Problem1.txt", 
        "MCP361_2021ME21063_Assignment7_Problem2.txt",
        "MCP361_2021ME21063_Assignment7_Problem3.txt", 
        "MCP361_2021ME21063_Assignment7_Problem4.txt",
        "MCP361_2021ME21063_Assignment7_Problem5.txt", 
        "MCP361_2021ME21063_Assignment7_Problem6.txt"
    ]
    # Process all files in the list
    process_multiple_files(game_file_list)

if __name__ == "__main__":
    main()  # Run the main function if the script is executed directly

