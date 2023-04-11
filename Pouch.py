from random import choices


class LetterPouch:
    def __init__(self):
        self.letters = list(
            '_' * 2 + 'a' * 9 + 'e' * 7 + 'i' * 8 + 'n' * 5 + 'o' * 6 + 'r' * 4 +
            's' * 4 + 'w' * 4 + 'z' * 5 + 'c' * 3 + 'd' * 3 + 'k' * 3 + 'l' * 3 +
            'm' * 3 + 'p' * 3 + 't' * 3 + 'y' * 4 + 'b' * 2 + 'g' * 2 + 'h' * 2 +
            'j' * 2 + 'ł' * 2 + 'u' * 2 +
            'ą' + 'ę' + 'f' + 'ó' + 'ś' + 'ż' + 'ć' + 'ń' + 'ź'
        )

    # TODO - ValueError: list.remove(x): x not in list
    def get_letters(self, number):
        random_letters = choices(self.letters, k=number)
        [self.letters.remove(letter) for letter in random_letters]
        return random_letters
