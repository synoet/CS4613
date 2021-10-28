def parse_file(filename):
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
