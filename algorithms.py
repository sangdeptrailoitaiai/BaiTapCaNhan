from collections import deque
import heapq
import random
import math
import time

class SearchNode:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

def extract_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    path.reverse()
    return path, len(path) - 1

def move(state, action):
    new_state = state[:]
    i = new_state.index(0)
    swap = -1
    if action == "up" and i >= 3: swap = i - 3
    elif action == "down" and i < 6: swap = i + 3
    elif action == "left" and i % 3 > 0: swap = i - 1
    elif action == "right" and i % 3 < 2: swap = i + 1
    if swap != -1:
        new_state[i], new_state[swap] = new_state[swap], new_state[i]
        return new_state
    return None

ACTIONS = ["up", "down", "left", "right"]

def bfs(initial, goal):
    frontier = deque([SearchNode(initial)])
    explored = set()
    while frontier:
        node = frontier.popleft()
        if node.state == goal:
            return extract_path(node)
        explored.add(tuple(node.state))
        for a in ACTIONS:
            ns = move(node.state, a)
            if ns and tuple(ns) not in explored:
                frontier.append(SearchNode(ns, node))
    return None, 0

def dfs(initial, goal, depth=100):
    stack = [SearchNode(initial)]
    explored = set()
    while stack:
        node = stack.pop()
        if node.state == goal:
            return extract_path(node)
        if node.cost < depth:
            explored.add(tuple(node.state))
            for a in ACTIONS:
                ns = move(node.state, a)
                if ns and tuple(ns) not in explored:
                    stack.append(SearchNode(ns, node, a, node.cost+1))
    return None, 0

def iterative_deepening(initial, goal, max_depth=50):
    for d in range(1, max_depth+1):
        result = dfs(initial, goal, d)
        if result: return result
    return None, 0

def manhattan(state, goal):
    dist = 0
    for i, val in enumerate(state):
        if val != 0:
            xi, yi = i % 3, i // 3
            xg, yg = goal.index(val) % 3, goal.index(val) // 3
            dist += abs(xi - xg) + abs(yi - yg)
    return dist

def greedy(initial, goal):
    frontier = [SearchNode(initial)]
    explored = set()
    while frontier:
        frontier.sort(key=lambda n: manhattan(n.state, goal))
        node = frontier.pop(0)
        if node.state == goal:
            return extract_path(node)
        explored.add(tuple(node.state))
        for a in ACTIONS:
            ns = move(node.state, a)
            if ns and tuple(ns) not in explored:
                frontier.append(SearchNode(ns, node, a, node.cost+1))
    return None, 0

def a_star(initial, goal):
    frontier = [SearchNode(initial)]
    explored = set()
    while frontier:
        frontier.sort(key=lambda n: n.cost + manhattan(n.state, goal))
        node = frontier.pop(0)
        if node.state == goal:
            return extract_path(node)
        explored.add(tuple(node.state))
        for a in ACTIONS:
            ns = move(node.state, a)
            if ns and tuple(ns) not in explored:
                frontier.append(SearchNode(ns, node, a, node.cost+1))
    return None, 0

def ucs(initial, goal):
    frontier = []
    heapq.heappush(frontier, (0, SearchNode(initial)))
    explored = set()
    cost_so_far = {tuple(initial): 0}
    while frontier:
        cost, node = heapq.heappop(frontier)
        if node.state == goal:
            return extract_path(node)
        explored.add(tuple(node.state))
        for a in ACTIONS:
            ns = move(node.state, a)
            if ns:
                nst = tuple(ns)
                new_cost = node.cost + 1
                if nst not in explored and (nst not in cost_so_far or new_cost < cost_so_far[nst]):
                    cost_so_far[nst] = new_cost
                    heapq.heappush(frontier, (new_cost, SearchNode(ns, node, a, new_cost)))
    return None, 0

def simulated_annealing(initial, goal):
    current = initial[:]
    current_cost = manhattan(current, goal)
    temp = 1.0
    cool = 0.99
    while temp > 0.01:
        a = random.choice(ACTIONS)
        ns = move(current, a)
        if not ns:
            temp *= cool
            continue
        new_cost = manhattan(ns, goal)
        if new_cost < current_cost or random.uniform(0, 1) < (current_cost - new_cost) / temp:
            current = ns
            current_cost = new_cost
        temp *= cool
    return [current], current_cost

def beam(initial, goal, width=3):
    frontier = [SearchNode(initial)]
    explored = set()
    while frontier:
        frontier.sort(key=lambda n: manhattan(n.state, goal))
        frontier = frontier[:width]
        node = frontier.pop(0)
        if node.state == goal:
            return extract_path(node)
        explored.add(tuple(node.state))
        for a in ACTIONS:
            ns = move(node.state, a)
            if ns and tuple(ns) not in explored:
                frontier.append(SearchNode(ns, node, a, node.cost+1))
    return None, 0

def hill_climbing(initial, goal):
    current = initial[:]
    current_cost = manhattan(current, goal)
    while True:
        best = None
        best_cost = current_cost
        for a in ACTIONS:
            ns = move(current, a)
            if ns:
                nc = manhattan(ns, goal)
                if nc < best_cost:
                    best = ns
                    best_cost = nc
        if best is None: break
        current = best
        current_cost = best_cost
        if current == goal: break
    return [current], current_cost

def steepest_hill_climbing(initial, goal):
    current = initial[:]
    path = [current[:]]
    current_cost = manhattan(current, goal)
    
    while True:
        best_neighbor = None
        best_cost = current_cost
        
        # Try all possible moves
        for action in ACTIONS:
            next_state = move(current, action)
            if next_state:
                neighbor_cost = manhattan(next_state, goal)
                if neighbor_cost < best_cost:
                    best_neighbor = next_state
                    best_cost = neighbor_cost
        
        if best_neighbor is None:
            break
            
        current = best_neighbor
        path.append(current[:])
        current_cost = best_cost
        
        if current == goal:
            break
    
    return path, len(path) - 1

def simulated_annealing_hc(initial, goal):
    current = initial[:]
    path = [current[:]]
    current_cost = manhattan(current, goal)
    
    temperature = 100.0
    cooling_rate = 0.95
    min_temperature = 0.1
    
    while temperature > min_temperature:
        for action in ACTIONS:
            next_state = move(current, action)
            if next_state:
                neighbor_cost = manhattan(next_state, goal)
                delta_cost = neighbor_cost - current_cost
                
                if delta_cost < 0 or random.random() < math.exp(-delta_cost / temperature):
                    current = next_state
                    path.append(current[:])
                    current_cost = neighbor_cost
                    
                    # If we reached the goal, we're done
                    if current == goal:
                        return path, len(path) - 1
        
        # Cool down
        temperature *= cooling_rate
    
    return path, len(path) - 1

def and_or(initial, goal):
    frontier = [SearchNode(initial)]
    explored = set()
    while frontier:
        node = frontier.pop(0)
        if node.state == goal:
            return extract_path(node)
        explored.add(tuple(node.state))
        for a in ACTIONS:
            ns = move(node.state, a)
            if ns and tuple(ns) not in explored:
                frontier.append(SearchNode(ns, node, a, node.cost+1))
    return None, 0

# --- New Algorithms ---
def iddfs(initial, goal):
    return iterative_deepening(initial, goal)

def search_no_observation(initial, goal, max_steps=1000):
    # Random walk, no observation
    state = initial[:]
    path = [state[:]]
    for _ in range(max_steps):
        a = random.choice(ACTIONS)
        ns = move(state, a)
        if ns:
            state = ns
            path.append(state[:])
            if state == goal:
                return path, len(path)-1
    return None, 0

def search_partial_observation(initial, goal, max_steps=1000):
    # Only knows position of empty cell
    state = initial[:]
    path = [state[:]]
    for _ in range(max_steps):
        empty_pos = state.index(0)
        # Only move based on empty cell position
        possible = []
        if empty_pos >= 3: possible.append("up")
        if empty_pos < 6: possible.append("down")
        if empty_pos % 3 > 0: possible.append("left")
        if empty_pos % 3 < 2: possible.append("right")
        a = random.choice(possible)
        ns = move(state, a)
        if ns:
            state = ns
            path.append(state[:])
            if state == goal:
                return path, len(path)-1
    return None, 0

def genetic_algorithm(initial, goal, pop_size=50, generations=200):
    def fitness(state):
        return -manhattan(state, goal)
    population = [initial[:]]
    for _ in range(pop_size-1):
        s = initial[:]
        for _ in range(random.randint(5, 20)):
            a = random.choice(ACTIONS)
            ns = move(s, a)
            if ns: s = ns
        population.append(s)
    for _ in range(generations):
        population.sort(key=fitness, reverse=True)
        if population[0] == goal:
            return [initial, population[0]], 1
        next_gen = population[:pop_size//2]
        while len(next_gen) < pop_size:
            p1, p2 = random.sample(next_gen, 2)
            cross = random.randint(1, 7)
            child = p1[:cross] + p2[cross:]
            if random.random() < 0.3:
                a = random.choice(ACTIONS)
                ns = move(child, a)
                if ns: child = ns
            next_gen.append(child)
        population = next_gen
    return None, 0

def backtracking(initial, goal, max_depth=30):
    def dfs(state, path, depth):
        if state == goal:
            return path + [state]
        if depth == 0:
            return None
        for a in ACTIONS:
            ns = move(state, a)
            if ns and ns not in path:
                res = dfs(ns, path + [state], depth-1)
                if res: return res
        return None
    res = dfs(initial, [], max_depth)
    if res:
        return res, len(res)-1
    return None, 0

def forward_tracking(initial, goal, max_depth=30):
    # Like backtracking but only forward moves (down, right)
    def dfs(state, path, depth):
        if state == goal:
            return path + [state]
        if depth == 0:
            return None
        for a in ["down", "right"]:
            ns = move(state, a)
            if ns and ns not in path:
                res = dfs(ns, path + [state], depth-1)
                if res: return res
        return None
    res = dfs(initial, [], max_depth)
    if res:
        return res, len(res)-1
    return None, 0

def stochastic_hill_climbing(initial, goal):
    current = initial[:]
    path = [current[:]]
    current_cost = manhattan(current, goal)
    while True:
        neighbors = []
        for a in ACTIONS:
            ns = move(current, a)
            if ns:
                neighbors.append((ns, manhattan(ns, goal)))
        better = [n for n in neighbors if n[1] < current_cost]
        if not better:
            break
        next_state, next_cost = random.choice(better)
        current = next_state
        current_cost = next_cost
        path.append(current[:])
        if current == goal:
            break
    return path, len(path)-1

def q_learning(initial, goal, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.2, max_steps=150):
    Q = {}
    ACTIONS = ['up', 'down', 'left', 'right']

    def h(state1, state2):
        # Heuristic khoảng cách Manhattan dạng phẳng
        return sum(1 for i in range(9) if state1[i] != state2[i])

    for ep in range(episodes):
        state = tuple(initial)
        for _ in range(max_steps):
            # Chọn hành động theo epsilon-greedy
            if random.random() < epsilon:
                action = random.choice(ACTIONS)
            else:
                q_values = [Q.get((state, a), 0) for a in ACTIONS]
                max_q = max(q_values)
                action = random.choice([a for a, q in zip(ACTIONS, q_values) if q == max_q])

            next_state = move(list(state), action)
            if not next_state:
                continue

            next_state_tuple = tuple(next_state)
            reward = 1 if next_state == goal else -h(next_state, goal)
            max_next_q = max(Q.get((next_state_tuple, a), 0) for a in ACTIONS)

            Q[(state, action)] = Q.get((state, action), 0) + alpha * (
                reward + gamma * max_next_q - Q.get((state, action), 0)
            )

            state = next_state_tuple
            if list(state) == goal:
                break

    # Trích xuất đường đi tốt nhất (greedy policy)
    state = tuple(initial)
    path = [list(state)]
    for _ in range(max_steps):
        q_values = [Q.get((state, a), 0) for a in ACTIONS]
        max_q = max(q_values)
        best_actions = [a for a, q in zip(ACTIONS, q_values) if q == max_q]
        action = random.choice(best_actions)
        next_state = move(list(state), action)
        if not next_state:
            break
        path.append(next_state)
        state = tuple(next_state)
        if next_state == goal:
            return path, len(path) - 1

    return path if path[-1] == goal else None, len(path) - 1

def ids(initial, goal, max_depth=50):
    """Iterative Deepening Search"""
    for depth in range(max_depth):
        result = dfs(initial, goal, depth)
        if result[0]:  # If solution found
            return result
    return None, 0

def ida_star(initial, goal, max_depth=100):
    """Iterative Deepening A* Search"""
    def search(node, g, bound):
        f = g + manhattan(node.state, goal)
        if f > bound:
            return f
        if node.state == goal:
            return extract_path(node)
        
        min_f = float('inf')
        for action in ACTIONS:
            next_state = move(node.state, action)
            if next_state:
                child = SearchNode(next_state, node, action, g + 1)
                result = search(child, g + 1, bound)
                if isinstance(result, tuple):  # Solution found
                    return result
                min_f = min(min_f, result)
        return min_f

    bound = manhattan(initial, goal)
    root = SearchNode(initial)
    
    while bound < max_depth:
        result = search(root, 0, bound)
        if isinstance(result, tuple):  # Solution found
            return result
        if result == float('inf'):  # No solution
            return None, 0
        bound = result
    
    return None, 0

def random_hill_climbing(initial, goal, max_iterations=1000):
    current = initial[:]
    path = [current[:]]
    current_cost = manhattan(current, goal)
    
    for _ in range(max_iterations):
        # Lấy ngẫu nhiên một hành động
        action = random.choice(ACTIONS)
        next_state = move(current, action)
        
        if next_state:
            next_cost = manhattan(next_state, goal)
            
            # Nếu trạng thái mới tốt hơn hoặc bằng trạng thái hiện tại
            if next_cost <= current_cost:
                current = next_state
                path.append(current[:])
                current_cost = next_cost
                
                # Nếu đạt được mục tiêu
                if current == goal:
                    return path, len(path) - 1
    
    return path, len(path) - 1

def min_conflicts(initial, goal, max_steps=1000):
    current = initial[:]
    path = [current[:]]
    
    for _ in range(max_steps):
        if current == goal:
            return path, len(path) - 1
            
        # Tìm vị trí của ô trống
        empty_pos = current.index(0)
        
        # Tính số xung đột cho mỗi hành động có thể
        conflicts = {}
        for action in ACTIONS:
            next_state = move(current, action)
            if next_state:
                # Số xung đột là số ô không đúng vị trí
                conflicts[action] = sum(1 for i in range(9) if next_state[i] != goal[i])
        
        if conflicts:
            # Chọn hành động có ít xung đột nhất
            min_conflict = min(conflicts.values())
            best_actions = [a for a, c in conflicts.items() if c == min_conflict]
            action = random.choice(best_actions)
            
            # Thực hiện hành động
            next_state = move(current, action)
            if next_state:
                current = next_state
                path.append(current[:])
    
    return path, len(path) - 1

def solve_with_algorithm(initial, goal, name):
    start_time = time.time()
    name = name.lower()
    if name == "bfs": result = bfs(initial, goal)
    elif name == "dfs": result = dfs(initial, goal)
    elif name == "iterative" or name == "iddfs": result = iddfs(initial, goal)
    elif name == "greedy": result = greedy(initial, goal)
    elif name == "a*": result = a_star(initial, goal)
    elif name == "ucs": result = ucs(initial, goal)
    elif name == "sa": result = simulated_annealing(initial, goal)
    elif name == "beam": result = beam(initial, goal)
    elif name == "hc": result = hill_climbing(initial, goal)
    elif name == "shc": result = steepest_hill_climbing(initial, goal)
    elif name == "sahc": result = simulated_annealing_hc(initial, goal)
    elif name == "and_or": result = and_or(initial, goal)
    elif name == "no_observation": result = search_no_observation(initial, goal)
    elif name == "partial_observation": result = search_partial_observation(initial, goal)
    elif name == "genetic": result = genetic_algorithm(initial, goal)
    elif name == "backtracking": result = backtracking(initial, goal)
    elif name == "forwardtracking" or name == "forward_tracking": result = forward_tracking(initial, goal)
    elif name == "stochastic_hc": result = stochastic_hill_climbing(initial, goal)
    elif name == "qlearning" or name == "q-learning": result = q_learning(initial, goal)
    elif name == "ids": result = ids(initial, goal)
    elif name == "ida_star": result = ida_star(initial, goal)
    elif name == "random_hc": result = random_hill_climbing(initial, goal)
    elif name == "min_conflicts": result = min_conflicts(initial, goal)
    else: result = None, 0
    end_time = time.time()
    execution_time = end_time - start_time
    if result:
        solution, cost = result
        return solution, cost, execution_time
    return None, 0, execution_time
