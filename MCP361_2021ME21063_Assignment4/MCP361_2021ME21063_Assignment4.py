def calculate_net_requirements(initial_inventory, receipts, demand, periods):
    """
    Calculate the net requirements for an item over a specified number of periods.
    """
    net_requirements = []  # List to store net requirements for each period
    inventory = initial_inventory  # Initialize inventory with the given initial inventory
    receipt_index = 0  # Index to track which receipt is being used

    for period in range(periods):
        available_inventory = inventory - demand[period]  # Calculate available inventory after meeting demand

        if available_inventory >= 0:
            # If inventory is sufficient to meet demand, no net requirement
            inventory = available_inventory
            net_requirements.append(0)
        else:
            # If inventory is insufficient, check for scheduled receipts
            while receipt_index < len(receipts) and available_inventory < 0:
                available_inventory += receipts[receipt_index]  # Add scheduled receipts to inventory
                receipt_index += 1

            if available_inventory >= 0:
                # If inventory is now sufficient after receipts, no net requirement
                inventory = available_inventory
                net_requirements.append(0)
            else:
                # If still insufficient, record shortage as net requirement
                shortage = -available_inventory
                inventory = 0  # Set inventory to zero since demand can't be met
                net_requirements.append(shortage)

    return net_requirements  # Return the list of net requirements

def propagate_demand(parent_net_req, multiplier=1):
    """
    Propagate demand to child components by applying a multiplier.
    """
    return [req * multiplier for req in parent_net_req]  # Multiply each net requirement by the multiplier

def calculate_all_requirements(components, initial_inventory, scheduled_receipts, demand_mapping):
    """
    Calculate net requirements for all components based on dependencies and demand mappings.
    """
    net_requirements = {}  # Dictionary to store net requirements for each component

    for component in components:
        if component not in net_requirements:
            # Calculate net requirements for the component if not already calculated
            net_requirements[component] = calculate_net_requirements(
                initial_inventory[component],
                scheduled_receipts[component],
                demand_mapping[component],
                len(demand_mapping[component])
            )
        # Propagate demand to dependent (child) components
        for child, multiplier in components[component].items():
            if child not in demand_mapping:
                demand_mapping[child] = [0] * len(demand_mapping[component])  # Initialize demand if not already present
            propagated_demand = propagate_demand(net_requirements[component], multiplier)  # Get propagated demand
            demand_mapping[child] = [
                demand_mapping[child][i] + propagated_demand[i] for i in range(len(propagated_demand))
            ]  # Update demand for child component by adding propagated demand

    return net_requirements  # Return the dictionary of net requirements


def main():
    # Components with their dependencies and multipliers
    components = {
        'A': {'B': 1, 'C': 2},  # A impacts B with 1:1 ratio and C with 2:1 ratio
        'B': {'C': 1},           # B impacts C with 1:1 ratio
        'C': {}                  # C has no dependent components
    }

    # Input Data
    demand_mapping = {
        'A': [15, 20, 30, 10, 30, 30, 30, 30],  # Only demand for A is initially known
    }
    initial_inventory = {
        'A': 30,
        'B': 60,
        'C': 60
    }
    scheduled_receipts = {
        'A': [20, 10],
        'B': [10],
        'C': [20, 10]
    }

    # Calculate all net requirements
    net_requirements = calculate_all_requirements(components, initial_inventory, scheduled_receipts, demand_mapping)

    # Output the results
    for component, reqs in net_requirements.items():
        print(f"Net requirements for component {component}: {reqs}")

# Run the main function
if __name__ == "__main__":
    main()
