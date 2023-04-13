class Tile:
    def __init__(self, letter=' ', bonus=None):
        self.letter = letter
        self.bonus = bonus


class ScrabbleBoard:
    def __init__(self):
        self.board = self._board_init()

    @staticmethod
    def _board_init():
        board = list()
        for _ in range(15):
            board.append(list())
            for _ in range(15):
                board[-1].append(Tile(letter='#'))
        return board

    def print_board(self):
        for row in self.board:
            for tile in row:
                print(tile.letter, end='  ')
            print(end='\n')

    def place_word(self, word: str, row: int, column: int, is_vertical=False):
        for shift, letter in enumerate(word):
            if is_vertical:
                self.board[row + shift][column].letter = letter
            else:
                self.board[row][column + shift].letter = letter

