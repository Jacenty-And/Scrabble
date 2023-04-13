from Scraper import Scraper
from Pouch import LetterPouch
from Bot import ScrabbleBot
from Board import ScrabbleBoard

if __name__ == '__main__':
    scrapper = Scraper()
    scrapper.run()
    scrapper.run_no_threading()

    board = ScrabbleBoard()
    board.print_board()

    bag = LetterPouch()
    letters = bag.get_letters(7)
    print(letters)
    [print(x, end='') for x in letters]
    print()

    bot = ScrabbleBot()
    best_word = bot.get_best_word(letters)
    print(best_word)

    board.place_word(best_word[1], 7, 7)
    board.print_board()

    print(bot.get_evaluated_and_sorted(letters))
