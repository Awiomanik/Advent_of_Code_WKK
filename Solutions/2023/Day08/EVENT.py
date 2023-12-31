# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 8

# PARAMETERS
data_path = "DATA.txt"

# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')
    INSTRUCTION = [direction for direction in data[0]]
    SETS = {key[:3]: value for key, value in \
                zip( \
                    data[2:], \
                    [{'L': left[7:10], 'R': right[12:15]} \
                        for left, right in zip(data[2:], data[2:])] \
                )}

    #print("DATA:\n", data)
    #print("INSTRUCTION:\n", INSTRUCTION)
    #print("SETS:\n", SETS)


# UTILITY FUNCTIONS
def walk():
    '''Counts number of steps between node 'AAA' and 'ZZZ' '''
    instruction_index = 0
    max_index = len(INSTRUCTION)
    current_state = "AAA"
    steps = 1

    while True:
        #print(steps, current_state, instruction_index)
        # reset index if past the limit
        if instruction_index == max_index:
            instruction_index = 0

        # calculate new position
        current_state = SETS[current_state][INSTRUCTION[instruction_index]]

        # check for last node
        if current_state == "ZZZ":
            break

        # increment indexes
        instruction_index += 1
        steps += 1
    
    return steps

def walk_unbounded_by_laws_of_spacetime_also_known_as_quantum_superposition_walk(state):
    '''Calculate number of steps form node state to first node ending in 'Z' '''
    instruction_index = 0
    max_index = len(INSTRUCTION)
    current_state = state
    steps = 1

    while True:
        #print(steps, current_state, instruction_index)
        # reset index if past the limit
        if instruction_index == max_index:
            instruction_index = 0

        # calculate new position
        current_state = SETS[current_state][INSTRUCTION[instruction_index]]

        # check for last node
        if current_state[2] == 'Z':
            break

        # increment indexes
        instruction_index += 1
        steps += 1
    
    return steps

def gcd(a, b):
    '''Greatest Common Devisor'''
    while b:
        a, b = b, a % b
    return a

def lcm_of_list(list):
    '''Least Common Multiple of a list of numbers'''
    resoult = list[0]

    for i in list[1:]:
        resoult = abs(resoult * i) // gcd(resoult, i)

    return resoult


def star1():
    print("steps (star1):", walk())

def star2():
    current_states = [node for node in SETS.keys() if node[2] == 'A']

    steps_per_node = []
    for state in current_states:
        steps_per_node.append(walk_unbounded_by_laws_of_spacetime_also_known_as_quantum_superposition_walk(state))

    print("steps (star2):", lcm_of_list(steps_per_node))

star1()
star2()