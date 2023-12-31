# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 9

from functools import reduce

# PARAMETERS
data_path = "DATA.txt"


# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')
    data = [[int(num) for num in seq] for seq in [d.split() for d in data]]
    #print("DATA:\n", data)


# UTILITY FUNCTIONS
def diff(seq):
    return [seq[i] - seq[i-1] for i in range(1, len(seq))]

def recursive_diff(seq, list_of_sequences=None, extrapolating_back=False):
    # set initial list
    if list_of_sequences == None:
        list_of_sequences = []

    # recursion escape condition
    if not any(seq):
        return list_of_sequences

    # add current value to return list
    if extrapolating_back:
        element2return = seq[0]
    else:
        element2return = seq[-1]
    list_of_sequences.append(element2return)

    # recursive diff
    seq = diff(seq)
    recursive_diff(seq, list_of_sequences, extrapolating_back)

    return list_of_sequences

def list_add(l):
    return reduce(lambda x, y: x+y, [num for num in l[::-1]])

def list_sutract(l):
    return reduce(lambda x, y: y-x, [num for num in l[::-1]])
        

def star1():
    print("star1:", sum([list_add(recursive_diff(d)) for d in data]))

def star2():
    print("star2:", sum([list_sutract(recursive_diff(d, extrapolating_back=True)) for d in data]))


star1()
star2()