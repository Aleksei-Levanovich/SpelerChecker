import math
from statistics import mean, mode

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


def check_word_spelling(set_of_words, word_to_check, top):
    top_hamming = []
    top_levenshtein = []
    top_jaccard = []
    min_hamming = 999
    min_levenshtein = 999
    min_jaccard = 999
    best_hamming = []
    best_levenshtein = []
    best_jaccard = []
    for word in set_of_words:
        if word == word_to_check:
            return 0
        if word != "":
            coefficients_ = get_coefficient_for_all_algoritms(word_to_check, word)
            top_hamming.append(coefficients_[0])
            top_levenshtein.append(coefficients_[1])
            top_jaccard.append(coefficients_[2])
            top_hamming = sorted(top_hamming, key=lambda i: i['coeff'])[:top]
            top_levenshtein = sorted(top_levenshtein, key=lambda i: i['coeff'])[:top]
            top_jaccard = sorted(top_jaccard, key=lambda i: i['coeff'])[:top]
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
    return top_hamming, best_hamming, top_levenshtein, best_levenshtein, top_jaccard, best_jaccard


def get_words_list(words_list):
    words = []
    for word in words_list:
        words.append(word['word'])
    return words


def get_metrics(word_correct, result0, result1, algo_name):
    best_words = get_words_list(result1)
    top_words = get_words_list(result0)
    if len(best_words) > len(top_words):
        top_words = best_words.copy()
        result0 = result1.copy()
    print(f"Количество наиболее похожих слов по алгоритму {algo_name}: {len(result1)}")
    flag_best = 0
    flag_top = 0
    if word_correct in best_words:
        print(f"Правильное слово \'{word_correct}\' содержится в самых похожих словах")
        flag_best = 1
    else:
        print(f"Правильное слово \'{word_correct}\' отсутствует в самых похожих словах")
    if word_correct in top_words:
        print(f"Правильное слово \'{word_correct}\' содержится в топ {len(top_words)} похожих словах")
        flag_top = 1
    else:
        print(f"Правильное слово \'{word_correct}\' отсутствует в топ {len(top_words)} похожих словах")
    print(f"Самые похожие слова:\n{result1}")
    print(f"Топ {len(top_words)} слов:\n{result0}")
    print("#######################################################")
    return flag_best, flag_top, len(best_words)


if __name__ == '__main__':
    set_of_words = set()
    set_of_words = set_of_words | split_text('voina-i-mir.txt')
    set_of_words = set_of_words | split_text('Enciklopediya.txt')
    set_of_words = set_of_words | split_text('wiki.txt')
    words_correct = ["блокнот", "восторжествовал", "галерея", "гарантировать", "гостиница", "дисциплина",
                      "достопримечательность", "изобразительный", "искусный", "искусственный", "непримиримый",
                      "обаяние", "обоняние", "обязанность", "официальный", "организация", "оптимист", "пессимизм"]
    # words_error = ["блакнот", "всторжевствовал", "галирея", "гаранировать", "гастинеца", "дестциплина",
    #                 "дастопримечетелность", "исобразительний", "изкусний", "искуственый", "непремеримый",
    #                 "абаяниё", "обаняние", "обязаностъ", "офисиалъный", "органызацыя", "аптымист", "песимизм"]
    words_error = ["блакнот", "всторжевствовал", "галирея", "гаранировать", "гастинеца", "дестциплина",
                     "дастопримечетелность", "исобразительний", "изкусний", "искуственый", "непремеримый"]
    top = 10
    hamming_flags_best = []
    levenshtein_flags_best = []
    jaccard_flags_best = []

    hamming_flags_top = []
    levenshtein_flags_top = []
    jaccard_flags_top = []

    hamming_avg = []
    levenshtein_avg = []
    jaccard_avg = []

    correct_predictions = []

    i = 0
    for word in words_error:
        result = check_word_spelling(set_of_words, word, top)
        print("#######################################################")
        print("#######################################################")
        print("#######################################################")
        if result == 0:
            print(f"Слово \"{word}\" присутсвует в словаре")
        else:
            print(f"Слово \"{word}\" ошибочное")
            print(f"Правильное слово: \"{words_correct[i]}\"")
            hamming_flag_best, hamming_flag_top, hamming_best_amount = get_metrics(words_correct[i], result[0], result[1], "Hamming")
            hamming_flags_best.append(hamming_flag_best)
            hamming_flags_top.append(hamming_flag_top)
            hamming_avg.append(hamming_best_amount)
            levenshtein_flag_best, levenshtein_flag_top, levenshtein_best_amount = get_metrics(words_correct[i], result[2], result[3], "Levenshtein")
            levenshtein_flags_best.append(levenshtein_flag_best)
            levenshtein_flags_top.append(levenshtein_flag_top)
            levenshtein_avg.append(levenshtein_best_amount)
            jaccard_flag_best, jaccard_flag_top, jaccard_best_amount = get_metrics(words_correct[i], result[4], result[5], "Jaccard")
            jaccard_flags_best.append(jaccard_flag_best)
            jaccard_flags_top.append(jaccard_flag_best)
            jaccard_avg.append(jaccard_best_amount)
            # metrics
            suggestion = ""
            if len(get_words_list(result[3])) == 2 and len(get_words_list(result[1])) > 3:
                suggestion = get_words_list(result[3])[0]
            elif len(get_words_list(result[3])) == 1:
                suggestion = get_words_list(result[3])[0]
            else:
                suggested_words = get_words_list(result[1])
                suggested_words.extend(get_words_list(result[3]))
                suggested_words.extend(get_words_list(result[5]))
                suggestion = mode(suggested_words)
            print(f"ПРЕДЛАГАЕМОЕ СЛОВО ДЛЯ ЗАМЕНЫ: {suggestion}")
            if suggestion == words_correct[i] or hamming_dist(suggestion, words_correct[i]) <= 1:
                correct_predictions.append(1)
            else:
                correct_predictions.append(0)
            i += 1
    print(f"Hamming.\n"
          f"Процент слов корректно предложенных к исправлению среди лучших вариантов: "
          f"{mean(hamming_flags_best) * 100}%\n"
          f"Процент слов корректно предложенных к исправлению среди топ-{top} вариантов: "
          f"{mean(hamming_flags_top) * 100}%\n"
          f"Среднее количество предлагаемых слов: {mean(hamming_avg)}")
    print(f"Levenshtein.\nПроцент слов корректно предложенных к исправлению среди лучших вариантов: "
          f"{mean(levenshtein_flags_best) * 100}%\n"
          f"Процент слов корректно предложенных к исправлению среди топ-{top} вариантов: "
          f"{mean(levenshtein_flags_top) * 100}%\n"
          f"Среднее количество предлагаемых слов: {mean(levenshtein_avg)}")
    print(f"Jaccard.\nПроцент слов корректно предложенных к исправлению среди лучших вариантов: "
          f"{mean(jaccard_flags_best) * 100}%\n"
          f"Процент слов корректно предложенных к исправлению среди топ-{top} вариантов: "
          f"{mean(jaccard_flags_top) * 100}%\n"
          f"Среднее количество предлагаемых слов: {mean(jaccard_avg)}")
    print(f"Приложение отработало корректно в {mean(correct_predictions) * 100}% случаев"
          f"(с учётом погрешности в 1 букву)")
