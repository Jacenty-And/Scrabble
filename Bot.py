from typing import List, Tuple
from Dictionary import ScrabbleDict


class ScrabbleBot:
    def __init__(self):
        self.dict = ScrabbleDict('dict_PL', 'D:/scrabble_dict/')
        self.points_dict = {
            'a': 1, 'ą': 5, 'b': 3, 'c': 2, 'ć': 6, 'd': 2, 'e': 1, 'ę': 5,
            'f': 5, 'g': 3, 'h': 3, 'i': 1, 'j': 3, 'k': 2, 'l': 2, 'ł': 3,
            'm': 2, 'n': 1, 'ń': 7, 'o': 1, 'ó': 5, 'p': 2, 'r': 1, 's': 1,
            'ś': 5, 't': 2, 'u': 3, 'w': 1, 'y': 2, 'z': 1, 'ź': 9, 'ż': 5,
            'q': 0, 'x': 0, 'v': 0, '_': 0
        }

    def evaluate_word(self, word) -> int:
        points = 0
        for letter in word:
            points += self.points_dict[letter]
        return points

    def evaluate_and_sort_by_points(self, words) -> List[Tuple[int, str]]:
        evaluated = [(self.evaluate_word(word), word) for word in words]
        sorted_by_points = sorted(evaluated, key=lambda x: x[0], reverse=True)
        return sorted_by_points

    def get_evaluated_and_sorted(self, letters) -> List[Tuple[int, str]]:
        words = self.dict.get_all_possible_from_letters(letters)
        evaluated_and_sorted = self.evaluate_and_sort_by_points(words)
        return evaluated_and_sorted

    def get_best_word(self, letters) -> Tuple[int, str]:
        evaluated_and_sorted = self.get_evaluated_and_sorted(letters)
        best_word = evaluated_and_sorted[0]
        return best_word
