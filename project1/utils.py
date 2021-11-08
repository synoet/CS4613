import sys

def parse_file(filename):
    """
    Util function to parse inputs
    Returns the initial and goal state in an array
    """
    initial_state = []
    goal_state = []
    lines = open(filename, 'r').readlines()
    switch = False
    for line in lines:
        if line == '\n':
            switch = True
        else:
            curr_line = line[:-1].split(' ')
            if switch:
                goal_state.append(curr_line)
            else:
                initial_state.append(curr_line)
    return[initial_state, goal_state]

def parse_args():
    """
    Parse arguements given to mainloop
    Generates a config that will run
    Controls wether or not debug mode runs
    """
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


def print_states_on_path(path):
    """
    Used in debug mode
    prints graphical board with f(n), g(n), and h(n)
    """
    counter = 1
    for node in path:
        print(f"({counter})")
        print(f"fn(n) = {node.value()}")
        print(node.board)
        counter += 1


def get_path_data(path, n, weight):
    """
    Returns list of actions and values
    Used in data needed to write to file
    """
    return [len(path), n , [node.action for node in path], [node.value() for node in path], weight]



def print_summary(initial_state, goal_state, path, n, weight):
    """
    Prints summary in format provided
    This output is then later used and piped into a file
    """
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


