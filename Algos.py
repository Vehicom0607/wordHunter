# Takes in a dictionary of words and returns a list of words in order
import math
# word_coords is a dictionary
# Each key is a list of words of that length from (3... n), where n is the length of the longest word
#   note: there will not necessarily be a key for every single number from 3 -> n
# This file will output the words in a list in the order that they should be claimed by the robot
points_dict = {
    3: 100,
    4: 400,
    5: 800,
    6: 1400,
    7: 1800,
    8: 2200,
    9: 2600,
    10: 3000,
    11: 3400,
    12: 3800,
    13: 4200,
    14: 4600,
    15: 5000,
    16: 10000
}

def euclidian_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)
def find_expected_score(claimed_words):
    score = 0
    for word in claimed_words:
        score += points_dict[len(word)]
    return score
def by_biggest(word_dict):
    ordered_word_list = []

    # Find the length of the biggest word
    biggest_len = 0
    for key in word_dict:
        biggest_len = max(key, biggest_len)

    while biggest_len >= 3:
        if biggest_len not in word_dict: # If there are no words of such length
            biggest_len -= 1
            continue

        for word in word_dict[biggest_len]:
            ordered_word_list.append(word)
        biggest_len -= 1

    # Returns in the format [] of [coords, word_string]
    # coords is a [] of (x, y)s
    # word_string is the word in string form
    return ordered_word_list


def greedy_biggest(word_dict):
    ordered_word_list = []
    pos = [0, 0]
    # Find the length of the biggest word
    biggest_len = 0
    for key in word_dict:
        biggest_len = max(key, biggest_len)

    while biggest_len >= 3:
        if biggest_len not in word_dict:  # If there are no words of such length
            biggest_len -= 1
            continue

        # It's not worth going through every possibility(esp for 3 length)
        # Using a greedy algo
        while len(word_dict[biggest_len]) > 0:
            closest = word_dict[biggest_len][0]
            for word in range(len(word_dict[biggest_len])):
                if euclidian_distance(pos, word_dict[biggest_len][word][0][0]) < euclidian_distance(pos, closest[0][0]):
                    closest = word_dict[biggest_len][word]
            ordered_word_list.append(closest)
            pos = closest[0][-1]
            word_dict[biggest_len].remove(closest)
        biggest_len -= 1

    # Returns in the format [] of [coords, word_string]
    # coords is a [] of (x, y)s
    # word_string is the word in string form
    return ordered_word_list
