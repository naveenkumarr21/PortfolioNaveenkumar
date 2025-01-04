import numpy as np

rows, cols = 3, 4
values = np.zeros((rows, cols))
rewards = np.zeros((rows, cols))
rewards[0, 3] = 1
rewards[1, 3] = -10
gamma = 0.9

actions = ['up', 'down', 'left', 'right']
action_moves = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}

state_labels = {index: f's{index + 1}' for index in range(rows * cols)}

def value_iteration(values, rewards, gamma, threshold=1e-4):
    rows, cols = values.shape
    delta = float('inf')
    while delta > threshold:
        delta = 0
        for i in range(rows):
            for j in range(cols):
                if (i, j) == (0, 3) or (i, j) == (1, 3):
                    continue
                v = values[i, j]
                possible_values = []

                for action in actions:
                    di, dj = action_moves[action]
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if (ni, nj) == (1, 1):
                            continue
                        possible_values.append(rewards[ni, nj] + gamma * values[ni, nj])

                if possible_values:
                    values[i, j] = max(possible_values)
                delta = max(delta, abs(v - values[i, j]))
    return values

def extract_policy(values, rewards, gamma):
    rows, cols = values.shape
    policy = np.full((rows, cols), None)

    for i in range(rows):
        for j in range(cols):
            if (i, j) == (0, 3):
                policy[i, j] = 'goal'
                continue
            elif (i, j) == (1, 3):
                policy[i, j] = 'fire'
                continue
            elif (i, j) == (1, 1):
                policy[i, j] = 'wall'
                continue

            best_action = None
            best_value = -float('inf')
            for action in actions:
                di, dj = action_moves[action]
                ni, nj = i + di, j + dj
                if 0 <= ni < rows and 0 <= nj < cols:
                    if (ni, nj) == (1, 1):
                        continue
                    action_value = rewards[ni, nj] + gamma * values[ni, nj]
                    if action_value > best_value:
                        best_value = action_value
                        best_action = action

            policy[i, j] = best_action
    return policy

def find_optimal_path(start, policy):
    path = [start]
    current = start

    while policy[current] != 'goal' and policy[current] != 'fire':
        action = policy[current]
        if action is None:
            break
        di, dj = action_moves[action]
        current = (current[0] + di, current[1] + dj)
        path.append(current)
        if current == (0, 3) or current == (1, 3):
            break
    labeled_path = [state_labels[i * cols + j] for i, j in path]
    return labeled_path

values = value_iteration(values, rewards, gamma)
policy = extract_policy(values, rewards, gamma)

print("Values:")
for i in range(rows):
    for j in range(cols):
        state = state_labels[i * cols + j]
        print(f"{state}: {values[i, j]:.2f}", end='\t')
    print()

print("\nPolicy:")
for i in range(rows):
    for j in range(cols):
        state = state_labels[i * cols + j]
        print(f"{state}: {policy[i, j]}", end='\t')
    print()

start_state_input = input("Enter the starting state (e.g., s1, s2, ..., s12): ").strip()
start_state_index = {v: k for k, v in state_labels.items()}.get(start_state_input)

if start_state_index is not None:
    start_row, start_col = divmod(start_state_index, cols)
    start_state = (start_row, start_col)
    optimal_path = find_optimal_path(start_state, policy)
    print("Optimal path:", optimal_path)
else:
    print("Invalid starting position.")
