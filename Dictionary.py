from typing import List, AnyStr
from itertools import combinations


def read_from_file(name, path='') -> List[AnyStr]:
    with open(f'{path}{name}.txt', 'r', encoding='UTF8') as txt_file:
        lines = txt_file.readlines()
    return lines


class ScrabbleDict:
    def __init__(self, name, path):
        self.alphabet = 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż'
        self.dictionary = self.dictionary_init(name, path)

    def dictionary_init(self, name, path):
        dictionary = dict()
        lines = read_from_file(name, path)
        words_grouped = list()
        for line in lines:
            words_grouped.append(line.split())
        for letter_index, letter in enumerate(self.alphabet):
            dictionary[letter] = dict()
            for length in range(2, 16):
                dictionary[letter][length] = words_grouped[letter_index * 14 + length - 2]
        return dictionary

    def get_with_length(self, length) -> list:
        words = list()
        for letter in self.alphabet:
            words.extend(self.dictionary[letter][length])
        return words

    def get_starts_with(self, start) -> list:
        words = list()
        for length in range(len(start) + 1, 16):
            words.extend([word for word in self.dictionary[start[0]][length] if word.startswith(start)])
        return words

    def get_ends_with(self, end) -> list:
        words = list()
        for length in range(len(end) + 1, 16):
            words.extend([word for word in self.get_with_length(length) if word.endswith(end)])
        return words

    def get_contains_word(self, subword) -> list:
        words = list()
        for length in range(len(subword) + 1, 16):
            words.extend([word for word in self.get_with_length(length) if subword in word])
        return words

    @staticmethod
    def get_contains_all_letters(letters, words) -> list:
        selected = list()
        blank = "_"
        for word in words:
            if len(word) != len(letters):
                continue
            if blank in letters:
                sorted1 = sorted(letters)
                index1 = 0
                sorted2 = sorted(word)
                index2 = 0
                blank_num = letters.count(blank)
                for _ in range(len(letters) + blank_num):
                    if sorted1[index1] == blank:
                        if index1 < len(sorted1) - 1:
                            index1 += 1
                        continue
                    if sorted1[index1] != sorted2[index2]:
                        if blank_num > 0:
                            blank_num -= 1
                            if index2 < len(sorted2) - 1:
                                index2 += 1
                            continue
                        else:
                            break
                    if index1 < len(sorted1) - 1:
                        index1 += 1
                    if index2 < len(sorted2) - 1:
                        index2 += 1
                else:
                    selected.append(word)
            else:
                for letter1, letter2 in zip(sorted(letters), sorted(word)):
                    if letter1 != letter2:
                        break
                else:
                    selected.append(word)
        return selected

    @staticmethod
    def get_all_combinations(letters) -> list:
        combinations_list = list()
        for length in range(len(letters), 1, -1):
            for combination in combinations(letters, length):
                combinations_list.append(list(combination))
        return combinations_list

    def get_all_possible_from_letters(self, letters) -> list:
        possible_words = list()
        for combination in self.get_all_combinations(letters):
            words_with_length = self.get_with_length(len(combination))
            contains_all = self.get_contains_all_letters(combination, words_with_length)
            possible_words.extend(contains_all)
            possible_words = list(set(possible_words))
        return possible_words

    def is_word_valid(self, word) -> bool:
        return word in self.dictionary[word[0]][len(word)]
