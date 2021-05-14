import numpy as np
import re


def hamming_dist(seq1, seq2):
    count = 0
    min_length = min(len(seq1), len(seq2))
    if abs(len(seq1)-len(seq2)) > 2:
        return 1000
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
    return 1 - len(set1 & set2) / (len(set1 | set2))


def sorensen(seq1, seq2):
    set1, set2 = set(seq1), set(seq2)
    return 1 - (2 * len(set1 & set2) / (len(set1) + len(set2)))


def split_text(path):
    unique_words = set()
    with open(path, 'r') as f:
        for line in f:
            line = line.lower()
            line = re.sub("\-", " ", line)
            line = re.sub("\n", "", line)
            regex = re.compile("[а-я\s]+")
            line = regex.findall(line)
            line = " ".join(line)
            words_array = line.split(' ')
            for word in words_array:
                if word != '' or word != '\n':
                    unique_words.add(word)
    return unique_words


def get_coefficient_for_all_algoritms(seq1, seq2):
    return [{'word': seq2, 'coeff': hamming_dist(seq1, seq2)}, {'word': seq2, 'coeff': levenshtein(seq1, seq2)},
            {'word': seq2, 'coeff': jaccard(seq1, seq2)}
            # {'word': seq2, 'coeff': sorensen(seq1, seq2)}
            ]


if __name__ == '__main__':
    set_of_words = set()
    set_of_words = set_of_words | split_text('voina-i-mir.txt')
    set_of_words = set_of_words | split_text('Enciklopediya.txt')
    set_of_words = set_of_words | split_text('wiki.txt')
    word_to_check = "трова"
    top_hamming = []
    top_levenshtein = []
    top_jaccard = []
    min_hamming = 999
    min_levenshtein = 999
    min_jaccard = 999
    best_hamming = []
    best_levenshtein = []
    best_jaccard = []
    word_found = False
    for word in set_of_words:
        if word == word_to_check:
            print("Слово присутсвует в словаре")
            word_found = True
            break
        if word != "":
            coefficients_ = get_coefficient_for_all_algoritms(word_to_check, word)
            top_hamming.append(coefficients_[0])
            top_levenshtein.append(coefficients_[1])
            top_jaccard.append(coefficients_[2])
            top_hamming = sorted(top_hamming, key=lambda i: i['coeff'])[:10]
            top_levenshtein = sorted(top_levenshtein, key=lambda i: i['coeff'])[:10]
            top_jaccard = sorted(top_jaccard, key=lambda i: i['coeff'])[:10]
            if coefficients_[0]['coeff'] < min_hamming:
                min_hamming = coefficients_[0]['coeff']
                best_hamming.clear()
                best_hamming.append(coefficients_[0])
            elif coefficients_[0]['coeff'] == min_hamming:
                best_hamming.append(coefficients_[0])

            if coefficients_[1]['coeff'] < min_levenshtein:
                min_levenshtein = coefficients_[1]['coeff']
                best_levenshtein.clear()
                best_levenshtein.append(coefficients_[1])
            elif coefficients_[1]['coeff'] == min_levenshtein:
                best_levenshtein.append(coefficients_[1])

            if coefficients_[2]['coeff'] < min_jaccard:
                min_jaccard = coefficients_[2]['coeff']
                best_jaccard.clear()
                best_jaccard.append(coefficients_[2])
            elif coefficients_[2]['coeff'] == min_jaccard:
                best_jaccard.append(coefficients_[2])

    if not word_found:
        print(top_hamming)
        print(best_hamming)
        print("#########################")
        print(top_levenshtein)
        print(best_levenshtein)
        print("#########################")
        print(top_jaccard)
        print(best_jaccard)
        print("#########################")

