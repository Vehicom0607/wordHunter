import random

BOARD_SIZE = 4
alphabet = "abcdefghijklmnopqrstuvwxyz"


# board_raw = []
# for i in range(4):
#     row = []
#     for j in range(4):
#         row.append(input("Enter letter " + str(i*4 + j + 1) + ":"))
#     board_raw.append(row)
#
# print(board_raw)


class Letter:
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        if type(letter) == int:
            self.letter = alphabet[letter]
            self.letter_number = letter
        elif type(letter) == str:
            self.letter = letter
            self.letter_number = alphabet.find(letter)


# for testing
#board_raw = \
#    [['a', 'i', 'e', 'y'],
#     ['d', 't', 'x', 'c'],
#     ['r', 'm', 'g', 'h'],
#     ['u', 'e', 't', 'n']]
board_raw = [['l', 'd', 's', 'u'], ['c', 'g', 't', 'e'], ['n', 'a', 'e', 'a'], ['o', 't', 'd', 'b']]


board = []
for i in range(BOARD_SIZE):  # Create 26x26 array
    temp = []
    for j in range(BOARD_SIZE):
        temp.append(Letter(i, j, board_raw[i][j]))
    board.append(temp)


# Get all words from sowpods
f = open("sowpods.txt", 'r')
words = []
for line in f:
    if len(line[:-1]) > 2:
        words.append(line[:-1])
words[-1] = "zzzs"

# Sort into lists by first two letters
alphabet = "abcdefghijklmnopqrstuvwxyz"
sorted_words = []
for i in range(26):  # Create 26x26 array
    sorted_words.append([])
    for j in range(26):
        sorted_words[i].append([])

for word in words:
    indx_first_letter = alphabet.find(word[0])
    indx_second_letter = alphabet.find(word[1])
    sorted_words[indx_first_letter][indx_second_letter].append(word)

print(sorted_words)


def check_letter(x, y, sorted_words, board):
    # letter = [x, y], sorted_words = sorted_words = board = board
    letter_indx = board[x][y].letter_number

    valid_two_letters = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (0 <= x + i < BOARD_SIZE) and (0 <= y + j < BOARD_SIZE):
                ij = board[x + i][y + j]
                if (len(sorted_words[letter_indx][ij.letter_number])) > 0:
                    valid_two_letters.append(ij)
                else:
                    print("Invalid Pair: " + board[x][y].letter + ij.letter)

    return valid_two_letters


valid_letter_pairs = []
for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
        letters = check_letter(i, j, sorted_words, board)
        valid_letter_pairs.append(letters)


def find_words(letters, board, sorted_words):
    used = []
    for letter in letters:
        used.append([letter.x, letter.y])

    possible_words = sorted_words[letters[0].letter_number][letters[1].letter_number]
    current_stem = "".join([a.letter for a in letters])

    tail = letters[-1]  # last letter in stem
    found_stems = []
    found_words = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            added = False
            if (i == 0 and j == 0) or ([tail.x + i, tail.y + j] in used):  # If already used
                continue
            if (0 <= tail.x + i < BOARD_SIZE) and (0 <= tail.y + j < BOARD_SIZE):
                test_letter = board[tail.x + i][tail.y + j]
                if current_stem + test_letter.letter in possible_words:
                    found_words.append([*letters, test_letter])
                for dict_word in possible_words:
                    if dict_word.startswith(current_stem + test_letter.letter):
                        if not added:
                            found_stems.append([*letters.copy(), test_letter])
                            added = True

    return found_stems, found_words


final_words = []
for i in range(BOARD_SIZE * BOARD_SIZE):
    stems = []
    words = []
    y, x = [i % BOARD_SIZE, i // BOARD_SIZE]
    first_letter = board[x][y]
    for second_letter in valid_letter_pairs[i]:
        result_stems, result_words = find_words([first_letter, second_letter], board, sorted_words)
        final_words += result_words
        stems += result_stems  # technically unnecessary if i set it to return to stems
        while len(stems) > 0:
            new_stems, words = find_words(stems[0], board, sorted_words)
            stems += new_stems
            final_words += words
            stems.pop(0)
    continue

counts = {}
for final_word in final_words:
    print("".join([a.letter for a in final_word]))

    counts[len(final_word)] = counts.get(len(final_word), 0) + 1

random_word = random.choice(final_words)
print("Random word: " + "".join([a.letter for a in random_word]))
for letter in random_word:
    print(letter.x, ",", letter.y)

print(counts)

word_coords = {}
for final_word in final_words:
    coords = [(a.x, a.y) for a in final_word]
    if len(final_word) not in word_coords:
        word_coords[len(final_word)] = []
    word_coords[len(final_word)].append(coords)

print(word_coords)

