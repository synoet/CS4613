import copy
from utils import parse_file, parse_args, print_states_on_path, get_path_data, print_summary

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
        """
        Draws information about the node, aswell as the board
        Only used in Debug Mode
        """
        node_info = 'Node: \n \n'
        node_info += 'f(n): {0}'.format(self.path_cost + self.board.h) + '\n'
        node_info += 'g(n): {0}'.format(self.path_cost) + '\n'
        node_info += 'h(n): {0}'.format(self.board.h) + '\n'
        node_info += 'Expanded: ' + ('Yes' if (len(self.children) != 0) else 'No') + '\n'
        node_info += 'Visited: ' + ('Yes' if self.visited else 'No') + '\n'
        node_info += repr(self.board)
        return node_info

    def value(self):
        """
        Return f(n) with a weight applied to heuristic
        """
        return self.path_cost + (self.weight * self.board.h)

    def __lt__(self, other):
        """
        For comparison of values between nodes
        """
        return self.value() < other.value()

    def __eq__(self, other):
        """
        Boards are equal if their states are equal
        """
        return self.board.state == other.board.state

    def h(self):
        """
        Return heuristic of the board
        """
        return self.board.h

    def visit(self):
        """
        Mark node as visited
        """
        self.visited = True

    def expand(self):
        """
        Returns an object containing a board state, 
        aswell as the action needed to get to that state from the parent
        """
        moves = self.board.get_moves()
        for move in moves:
            self.children.append(Node(move["board"], self, move["action"], self.weight))


class Board:
    def __init__(self, state, goal_state):
        self.state = state
        self.goal_state = goal_state
        self.h = self.sum_m_d()

    def __repr__(self):
        """
        Draws a board with the tiles in the correct positions
        Only used for visual representations in debug mode
        """
        row_divider = '- - - - - - - - - \n'
        rep = row_divider
        for row in self.state:
            rep = rep + '| '
            for item in row:
                rep = rep + item + (' | ' if len(item) == 1 else '| ')
            rep = rep + '\n' + row_divider
        return rep

    def __eq__(self, other):
        """
        Two boards are equal if their states are equal
        """
        return self.state == other.state

    def is_goal(self):
        """
        A board is the goal if it has the goal_state
        """
        return self.state == self.goal_state

    def get_goal_pos(self, value):
        """
        Get the distance in rows and columns of a value from its goal state
        """
        for r in range(len(self.goal_state)):
            for c in range(len(self.goal_state[r])):
                if self.goal_state[r][c] == value:
                    return [r, c]

    def get_pos(self, value):
        """
        Return the position of any value of the board
        """
        for r in range(len(self.state)):
            for c in range(len(self.state[0])):
                if self.state[r][c] == value:
                    return [r, c]

    def sum_m_d(self):
        """
        Sum of Manhattan Distances
        returns the sum of the distance of every tile from its goal position
        """
        sum_value = 0
        for r in range(len(self.state)):
            for c in range(len(self.state[0])):
                if self.state[r][c] != self.goal_state[r][c] and self.state[r][c] != '0':
                    goal_r, goal_c = self.get_goal_pos(self.state[r][c])
                    sum_value = sum_value + abs(r - goal_r) + abs(c - goal_c)
        return sum_value

    def get_moves(self):
        """
        Returns an object with a possible action and its corresponding state
        This function is invoked by the Node class to expand a node
        """
        moves = []
        # get the position of the empty tile
        empty_r, empty_c = self.get_pos('0')

        # calculate states for available adjacent positions

        # Make sure that the current row is not the first row
        if empty_r > 0:
            # Copy the original state to create a new state
            new_state = copy.deepcopy(self.state)
            # Replace the position of the empty tile with the one below it
            new_state[empty_r][empty_c], new_state[empty_r - 1][empty_c] = new_state[empty_r - 1][empty_c], '0'
            # Create a new Board with the new state
            board_move_down = Board(new_state, self.goal_state)
            # Append the object with the action and state to the list
            moves.append({"action": "U", "board": board_move_down})

        # Make sure the current column is not the first column
        if empty_c > 0:
            # Copy the original state to create a new state
            new_state = copy.deepcopy(self.state)
            # Replace the position of the empty tile with the one to the left
            new_state[empty_r][empty_c], new_state[empty_r][empty_c - 1] = new_state[empty_r][empty_c - 1], '0'
            # Create a new Board with the new state
            board_move_right = Board(new_state, self.goal_state)
            # APpend the object with the action and state to the list
            moves.append({"action": "L", "board": board_move_right})

        # Make cure the current column is not the last column
        if empty_c < len(self.state[0]) - 1:
            # Copy the original state to create a new state
            new_state = copy.deepcopy(self.state)
            # Replace the position of the empty tile with the one to the right
            new_state[empty_r][empty_c], new_state[empty_r][empty_c + 1] = new_state[empty_r][empty_c + 1 ], '0'
            # Create a new Board with the new state
            board_move_left = Board(new_state, self.goal_state)
            # Append the object with the action and state to the list
            moves.append({"action": "R", "board": board_move_left})

        # Make sure the current row is now the last row
        if empty_r < len(self.state) - 1:
            # Copy the original state to create a new state
            new_state = copy.deepcopy(self.state)
            # Replace the position of the empty tile with the one above
            new_state[empty_r][empty_c], new_state[empty_r + 1][empty_c] = new_state[empty_r + 1][empty_c], '0'
            # Create a new board with the new state
            board_move_up = Board(new_state, self.goal_state)
            # Append the object with the action and state to the list
            moves.append({"action": "D", "board": board_move_up})

        return moves


def path_to_start(node, start_node):
    """
    Find the path from a goal node back to the start
    Reverse the list at the end to get the right direction
    """
    path = []
    while node != start_node:
        path.append(node)
        node = node.parent

    return path[::-1]

def is_visited(visited, node):
    """
    Return true if a node has already been visited
    Else return false
    """
    for visited_node in visited:
        if visited_node == node:
            return True
    return False


def search(initial_state, goal_state, weight):
    """
    Run A star on a given initial state and goal state
    Return path from the start node to goal node, aswell as the number of nodes generated
    """
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

if __name__ == '__main__':
    # Get configuration for running
    file_path, weight, debug_mode = parse_args()

    # parse initial_state and goal_state from file
    states = parse_file(file_path)

    # Run search and grab output
    initial_state, goal_state, path, n = search(states[0], states[1], weight)

    # If debug mode is turned out print boards
    # Else we write to file in the provided format
    if debug_mode:
        print_states_on_path(path)
    else:
        print_summary(initial_state, goal_state, path, n, weight)
  

