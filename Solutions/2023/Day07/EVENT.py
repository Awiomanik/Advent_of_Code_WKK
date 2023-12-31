# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 7

from functools import reduce

# PARAMETERS
data_path = "DATA.txt"

# CONSTANTS
CARD2INT = {
    'A': 12,
    'K': 11,
    'Q': 10,
    'J': 9,
    'T': 8,
    '9': 7,
    '8': 6,
    '7': 5,
    '6': 4,
    '5': 3,
    '4': 2,
    '3': 1,
    '2': 0
}

CARD2INT_WC = {
    'A': 12,
    'K': 11,
    'Q': 10,
    'J': 0,
    'T': 9,
    '9': 8,
    '8': 7,
    '7': 6,
    '6': 5,
    '5': 4,
    '4': 3,
    '3': 2,
    '2': 1    
}

CARDS_WITHOUT_WC = [ 'A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')
    hands, bids = [d[:5] for d in data], [int(d[6:]) for d in data]
    #print("DATA:\n", data)
    #print(hands)
    #print(bids)

# UTILITY FUNCTIONS
def compare_hands(hand1, hand2, original_hand1=None, original_hand2=None):
    '''
    Return True if hand1 is higher, else False
    If original_hands given in secound order comparison rule compares original_hands
    '''
    ht1, ht2 = hand_type(hand1), hand_type(hand2)

    if ht1 > ht2: return True
    if ht1 < ht2: return False

    # secound ordering rule comparison
    if original_hand1: return compare2order(original_hand1, original_hand2, CARD2INT_WC)
    return compare2order(hand1, hand2)

def hand_type(hand):
    '''
    Return type as int respectivelly:
    0 = High card
    1 = One pair
    2 = Two pair
    3 = Three of a kind
    4 = Full house
    5 = Four of a kind
    6 = Five of a kind  
    '''
    # format hand if necessary
    if type(hand) == type([]):
        hand = reduce(lambda x, y: x+y, hand)

    # find number of unique cards
    unique = set(hand)
    diff = len(unique)
    unique = list(unique)

    # Five of a kind
    if diff <= 1: return 6
    # Four of a kind / Full house
    if diff == 2: 
        # Four of a kind
        if hand.count(unique[0]) == 1 or hand.count(unique[1]) == 1: return 5
        # Full house
        else: return 4
    # Three of a kind / Two pair
    if diff == 3:
        # Three of a kind
        if any([hand.count(u) == 3 for u in unique]): return 3
        # Two pair
        else: return 2
    # One pair
    if diff == 4: return 1
    # High card
    return 0

def compare2order(hand1, hand2, mapping=CARD2INT):
    '''Return True if hand1 is higher according two secound ordering rule, else False'''
    for c1, c2 in zip(hand1, hand2):
        c1, c2 = mapping[c1], mapping[c2]

        if c1 > c2: return True
        if c1 < c2: return False
    
def quick_sort_hands(hands, bids):
    '''
    Sort hands and bids by hand type or secound ordering rule if necessary
    using quick sort algorithm
    '''
    # Escape recursion condition
    if len(hands) <= 1: return hands, bids

    # Devide into two arrays
    smaller = []
    s_bids = []
    higher = []
    h_bids = []

    for h, b in zip(hands[:-1], bids[:-1]):
        if compare_hands(hands[-1], h):
            smaller.append(h)
            s_bids.append(b)
        else:
            higher.append(h)
            h_bids.append(b)

    #print("HANDS:\t", hands, bids)
    #print("SMALLER:", smaller, s_bids)
    #print("HIGHER:\t", higher, h_bids)
    #print()

    # Built array through recursion
    sorted_s_h, sorted_s_b = quick_sort_hands(smaller, s_bids)
    sorted_h_h, sorted_h_b = quick_sort_hands(higher, h_bids)

    return sorted_s_h + [hands[-1]] + sorted_h_h, sorted_s_b + [bids[-1]] + sorted_h_b


def quick_sort_hands_wc(hands, bids, original_hands):
    '''
    Sort hands and bids by hand type or secound ordering rule if necessary
    using quick sort algorithm
    Takes into account wild cards
    '''
    # Escape recursion condition
    if len(hands) <= 1: return hands, bids, original_hands

    # Devide into two arrays
    smaller = []
    s_bids = []
    higher = []
    h_bids = []
    s_original = []
    h_original = []

    for h, b, o in zip(hands[:-1], bids[:-1], original_hands[:-1]):
        if compare_hands(hands[-1], h,original_hands[-1], o):
            smaller.append(h)
            s_bids.append(b)
            s_original.append(o)
        else:
            higher.append(h)
            h_bids.append(b)
            h_original.append(o)

    # Built array through recursion
    # sort subarrays
    sorted_s_h, sorted_s_b, sorted_s_o = quick_sort_hands_wc(smaller, s_bids, s_original)
    sorted_h_h, sorted_h_b, sorted_h_o = quick_sort_hands_wc(higher, h_bids, h_original)
    # build arrays
    sorted_hands = sorted_s_h + [hands[-1]] + sorted_h_h
    sorted_bids = sorted_s_b + [bids[-1]] + sorted_h_b
    sorted_original = sorted_s_o + [original_hands[-1]] + sorted_h_o

    return sorted_hands, sorted_bids, sorted_original

def generate_variations(hand, original_hand=None, index=0, variations=None):
    '''
    Takes list of chars represanting hand
    Returns list of lists of chars repersenting every possible hand,
            where wild card 'J' is swaped for any other card
    '''
    #print("generate:\n", hand, original_hand, variations)
    # unset default None values
    if variations == None:
        variations = ([],)

    if original_hand == None:
        original_hand = hand
        
    # recursion escape condition
    if index >= len(hand):
        #print("bottom", hand, variations)
        variations[0].append(hand)
        #print("var", variations)
        return variations[0], original_hand
    
    if hand[index] == 'J':
        # replace 'J' with each other card
        for card in CARDS_WITHOUT_WC:
            temp_hand = hand.copy()
            temp_hand[index] = card
            variations = generate_variations(temp_hand, original_hand, index+1, variations)
    else:
        # move to the next element if it's not 'J'
        variations = generate_variations(hand, original_hand, index+1, variations)
    
    return variations[0], original_hand

def find_highest_veriation(variations, original_hand):
    '''
    Find best hand in variations
    Return highesthand and original hand
    '''
    # Worst possible hand as first value to compare to later
    highest_hand = highest_original_hand = list('23456')

    # Loop through variations and find highest
    for v in variations:
        highest_hand = v \
            if compare_hands(v, highest_hand, original_hand, highest_original_hand) \
            else highest_hand
        
    return highest_hand, original_hand

def generate_wc_hands(hands_list):
    return zip(*[find_highest_veriation(*generate_variations(list(h))) \
                for h in hands_list])


def star1():
    _, bids_sorted = quick_sort_hands(hands, bids)

    print("star1:\t", sum([int(b)*(i+1) for i, b in enumerate(bids_sorted)]))

def star2():
    # Find best hands
    hands_wc, original_hands_wc = generate_wc_hands(hands)
    # sort hands
    bids_sorted = quick_sort_hands_wc(hands_wc, bids, original_hands_wc)[1]
    # resoult
    print("star2:\t", sum([(i+1)*b for i, b in enumerate(bids_sorted)]))
    
star1()
star2()
