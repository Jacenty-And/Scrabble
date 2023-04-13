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

