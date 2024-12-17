def fractional_bound(items, capacity, index, current_value, current_weight):
    if current_weight >= capacity:
        return current_value

    bound = current_value
    total_weight = current_weight
    for i in range(index, len(items)):
        value, weight = items[i]
        if total_weight + weight <= capacity:
            total_weight += weight
            bound += value
        else:
            fraction = (capacity - total_weight) / weight
            bound += value * fraction
            break
    return bound

def branch_and_bound_knapsack(items, capacity):
    items_with_index = sorted(
        [(v, w, i) for i, (v, w) in enumerate(items)], 
        key=lambda x: x[0]/x[1], 
        reverse=True
    )
    sorted_items = [(v, w) for v, w, i in items_with_index]

    stack = []
    stack.append((0, 0, 0, []))

    best_value = 0
    best_solution = []

    while stack:
        index, current_value, current_weight, taken = stack.pop()
        if index == len(items):
            if current_value > best_value:
                best_value = current_value
                best_solution = taken
            continue

        bound = fractional_bound(sorted_items, capacity, index, current_value, current_weight)

        if bound <= best_value:
            continue

        item_value, item_weight = sorted_items[index]
        if current_weight + item_weight <= capacity:
            stack.append((index + 1, 
                          current_value + item_value, 
                          current_weight + item_weight, 
                          taken + [1]))
        stack.append((index + 1, 
                      current_value, 
                      current_weight, 
                      taken + [0]))

    chosen_items_indices = []
    for (v,w,i), chosen in zip(items_with_index, best_solution):
        if chosen == 1:
            chosen_items_indices.append(i)

    return best_value, chosen_items_indices

def solve_knapsack_branch_and_bound(items, capacity):
    max_val, chosen_indices = branch_and_bound_knapsack(items, capacity)
    return max_val, chosen_indices


if __name__ == "__main__":
    capacity = 150
    revenues = [15, 20, 5, 25, 22, 17]
    days = [51, 60, 35, 60, 53, 10]

    items = list(zip(revenues, days))

    optimal_value, chosen_projects = solve_knapsack_branch_and_bound(items, capacity)

    print("Optimal total revenue:", optimal_value)
    chosen_project_numbers = [i+1 for i in chosen_projects]
    print("Chosen projects:", chosen_project_numbers)