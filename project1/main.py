import utils
import copy

class Node:
    def __init__(self, board, parent):
        self.board = board
        self.parent = parent
        self.path_cost = parent.path_cost + 1 if parent is not None else 0
        self.children = []
        self.visited= False

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
        return self.path_cost + self.board.h

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
            self.children.append(Node(move, self))


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
                if self.state[r][c] != self.goal_state[r][c] and self.state[r][c] != '_':
                    goal_r, goal_c = self.get_goal_pos(self.state[r][c])
                    sum_value = sum_value + abs(r - goal_r) + abs(c - goal_c)
        return sum_value

    def get_moves(self):
        moves = []
        # get the position of the empty tile
        empty_r, empty_c = self.get_pos('_')

        # calculate states for available adjacent positions

        if empty_r > 0:
            new_state = copy.deepcopy(self.state)
            new_state[empty_r][empty_c], new_state[empty_r - 1][empty_c] = new_state[empty_r - 1][empty_c], '_'
            board_move_down = Board(new_state, self.goal_state)
            moves.append(board_move_down)

        if empty_c > 0:
            new_state = copy.deepcopy(self.state)
            new_state[empty_r][empty_c], new_state[empty_r][empty_c - 1] = new_state[empty_r][empty_c - 1], '_'
            board_move_right = Board(new_state, self.goal_state)
            moves.append(board_move_right)

        if empty_c < len(self.state[0]) - 1:
            new_state = copy.deepcopy(self.state)
            new_state[empty_r][empty_c], new_state[empty_r][empty_c + 1] = new_state[empty_r][empty_c + 1 ], '_'
            board_move_left = Board(new_state, self.goal_state)
            moves.append(board_move_left)

        if empty_r < len(self.state) - 1:
            new_state = copy.deepcopy(self.state)
            new_state[empty_r][empty_c], new_state[empty_r + 1][empty_c] = new_state[empty_r + 1][empty_c], '_'
            board_move_up = Board(new_state, self.goal_state)
            moves.append(board_move_up)

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

def pretty_print(path):
    counter = 1
    for node in path:
        print(f"({counter})")
        print(f"fn(n) = {node.value()}")
        print(node.board)
        counter += 1


def search(initial_state, goal_state):
    initial_board = Board(initial_state, goal_state)

    initial_node = Node(initial_board, None)

    open = []
    visited = []

    open.append(initial_node)

    while len(open) > 0:

        open.sort()

        node = open.pop(0)

        node.visit()
        visited.append(node)

        if node.board.is_goal():
           return path_to_start(node, initial_node)

        node.expand()

        for child in node.children:
            if not is_visited(visited, child):
                open.append(child)


if __name__ == '__main__':
    states = utils.parse_file('test.txt')
    pretty_print(search(states[0], states[1]))

