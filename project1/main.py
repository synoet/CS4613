import utils
import copy
import sys

class Node:
    def __init__(self, board, parent, action, weight):
        self.board = board
        self.parent = parent
        self.path_cost = parent.path_cost + 1 if parent is not None else 0
        self.children = []
        self.visited= False
        self.action = action
        self.weight = weight if weight else 1.0

    def __repr__(self):
        node_info = 'Node: \n \n'
        node_info += 'f(n): {0}'.format(self.path_cost + self.board.h) + '\n'
        node_info += 'g(n): {0}'.format(self.path_cost) + '\n'
        node_info += 'h(n): {0}'.format(self.board.h) + '\n'
        node_info += 'Expanded: ' + ('Yes' if (len(self.children) != 0) else 'No') + '\n'
        node_info += 'Visited: ' + ('Yes' if self.visited else 'No') + '\n'
        node_info += repr(self.board)
        return node_info

    def value(self):
        return self.path_cost + (self.weight * self.board.h)

    def __lt__(self, other):
        return self.value() < other.value()

    def __eq__(self, other):
        return self.board.state == other.board.state

    def h(self):
        return self.board.h

    def visit(self):
        self.visited = True

    def expand(self):
        moves = self.board.get_moves()
        for move in moves:
            self.children.append(Node(move["board"], self, move["action"], self.weight))


class Board:
    def __init__(self, state, goal_state):
        self.state = state
        self.goal_state = goal_state
        self.h = self.sum_m_d()

    def __repr__(self):
        row_divider = '- - - - - - - - - \n'
        rep = row_divider
        for row in self.state:
            rep = rep + '| '
            for item in row:
                rep = rep + item + (' | ' if len(item) == 1 else '| ')
            rep = rep + '\n' + row_divider
        return rep

    def __eq__(self, other):
        return self.state == other.state

    def is_goal(self):
        return self.state == self.goal_state

    def get_goal_pos(self, value):
        for r in range(len(self.goal_state)):
            for c in range(len(self.goal_state[r])):
                if self.goal_state[r][c] == value:
                    return [r, c]

    def get_pos(self, value):
        for r in range(len(self.state)):
            for c in range(len(self.state[0])):
                if self.state[r][c] == value:
                    return [r, c]

    def sum_m_d(self):
        sum_value = 0
        for r in range(len(self.state)):
            for c in range(len(self.state[0])):
                if self.state[r][c] != self.goal_state[r][c] and self.state[r][c] != '0':
                    goal_r, goal_c = self.get_goal_pos(self.state[r][c])
                    sum_value = sum_value + abs(r - goal_r) + abs(c - goal_c)
        return sum_value

    def get_moves(self):
        moves = []
        # get the position of the empty tile
        empty_r, empty_c = self.get_pos('0')

        # calculate states for available adjacent positions

        if empty_r > 0:
            new_state = copy.deepcopy(self.state)
            new_state[empty_r][empty_c], new_state[empty_r - 1][empty_c] = new_state[empty_r - 1][empty_c], '0'
            board_move_down = Board(new_state, self.goal_state)
            moves.append({"action": "U", "board": board_move_down})

        if empty_c > 0:
            new_state = copy.deepcopy(self.state)
            new_state[empty_r][empty_c], new_state[empty_r][empty_c - 1] = new_state[empty_r][empty_c - 1], '0'
            board_move_right = Board(new_state, self.goal_state)
            moves.append({"action": "L", "board": board_move_right})

        if empty_c < len(self.state[0]) - 1:
            new_state = copy.deepcopy(self.state)
            new_state[empty_r][empty_c], new_state[empty_r][empty_c + 1] = new_state[empty_r][empty_c + 1 ], '0'
            board_move_left = Board(new_state, self.goal_state)
            moves.append({"action": "R", "board": board_move_left})

        if empty_r < len(self.state) - 1:
            new_state = copy.deepcopy(self.state)
            new_state[empty_r][empty_c], new_state[empty_r + 1][empty_c] = new_state[empty_r + 1][empty_c], '0'
            board_move_up = Board(new_state, self.goal_state)
            moves.append({"action": "D", "board": board_move_up})

        return moves


def path_to_start(node, start_node):
    path = []
    while node != start_node:
        path.append(node)
        node = node.parent

    return path[::-1]

def is_visited(visited, node):
    for visited_node in visited:
        if visited_node == node:
            return True
    return False

def print_states_on_path(path):
    counter = 1
    for node in path:
        print(f"({counter})")
        print(f"fn(n) = {node.value()}")
        print(node.board)
        counter += 1


def get_path_data(path, n, weight):
    return [len(path), n , [node.action for node in path], [node.value() for node in path], weight]

def print_summary(initial_state, goal_state, path, n, weight):
    output = ""
    for idx in range(len(initial_state)):
        for jdx in range(len(initial_state[0])):
            output += f"{initial_state[idx][jdx]} "
        output += "\n"
    output += "\n"
    for idx in range(len(goal_state)):
        for jdx in range(len(goal_state[0])):
            output += f"{goal_state[idx][jdx]} "
        output += "\n"
    output += "\n"
    d, n, a_list, f_list, w = get_path_data(path, n, weight)
    output += f"{w} \n{d} \n{n}\n"
    for a in a_list:
        output += f"{a} "
    output += "\n"
    for f in f_list:
        output += f"{f} "
    
    print(output)


def search(initial_state, goal_state, weight):
    # Initialize initial board state
    initial_board = Board(initial_state, goal_state)

    # Initialize node with board state
    initial_node = Node(initial_board, None, None, weight)

    # Number of Nodes Generated
    n = 1

    # Current Unvisited Nodes
    open = []

    # Visited Nodes
    visited = []

    # Add initial node to the list of open nodes
    open.append(initial_node)

    # While we have nodes to visit we dont stop searching
    while len(open) > 0:

        # Use lt of node to compare f(n) valalue of each node and sort by lowest
        open.sort()

        # Current node becomes the node with lowest possible value
        node = open.pop(0)

        # Mark node as visited
        node.visit()

        # Append node to visited list
        visited.append(node)

        # Check if node's board state is the goal state
        # If it is the goal state we trace a path back to start and return
        if node.board.is_goal():
           return [initial_state, goal_state, path_to_start(node, initial_node), n]

        # Populates node.children with possible variations
        node.expand()

        # Go through all children and check if it has been visited
        # If the node has not been visited we add it to open
        for child in node.children:
            if not is_visited(visited, child):
                open.append(child)
                n += 1

    # Return None if noo path was found
    return None

def parse_args():
    file_path = './inputs/input1.txt'
    weight = 1.0
    debug = False

    for idx in range(len(sys.argv)):
        if sys.argv[idx] == "-f":
            file_path = f"{sys.argv[idx + 1]}"
            idx += 1
        elif sys.argv[idx] == "-w":
            weight = float(sys.argv[idx + 1])
            idx += 1
        elif sys.argv[idx] == "--debug":
            debug = True
    return [file_path, weight, debug]

if __name__ == '__main__':
    file_path, weight, debug_mode = parse_args()

    states = utils.parse_file(file_path)

    initial_state, goal_state, path, n = search(states[0], states[1], weight)

    if debug_mode:
        print_states_on_path(path)
    else:
        print_summary(initial_state, goal_state, path, n, weight)
  

