import numpy as np
import re

def hamming_dist(seq1, seq2):
    count = 0
    min_length = min(len(seq1), len(seq2))
    for i in range(0, min_length):
        if seq1[i] != seq2[i]:
            count += 1
    return count


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1] + 1,
                    matrix[x, y-1] + 1
                )
    return matrix[size_x - 1, size_y - 1]


def jaccard(seq1, seq2):
    set1, set2 = set(seq1), set(seq2)
    return 1 - len(set1 & set2) / float(len(set1 | set2))


def sorensen(seq1, seq2):
    set1, set2 = set(seq1), set(seq2)
    return 1 - (2 * len(set1 & set2) / float(len(set1) + len(set2)))


def split_text(path):
    unique_words = set()
    with open(path, 'r') as f:
        for line in f:
            line = line.lower()
            line = re.sub("\-", " ", line)
            regex = re.compile("[а-я\s]+")
            line = regex.findall(line)
            line = " ".join(line)
            words_array = line.split(' ')
            for word in words_array:
                if word != '' or word != '\n':
                    unique_words.add(word)
    return unique_words


if __name__ == '__main__':
    set_of_words = split_text('Vedmak.txt')
    print(sorensen('a', 'b'))
