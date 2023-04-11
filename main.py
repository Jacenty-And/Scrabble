from Scraper import Scraper
from Pouch import LetterPouch
from Bot import ScrabbleBot

if __name__ == '__main__':
    scrapper = Scraper()
    scrapper.run()
    scrapper.run_no_threading()

    bag = LetterPouch()
    letters = bag.get_letters(7)
    print(letters)
    [print(x, end='') for x in letters]
    print()

    bot = ScrabbleBot()
    print(bot.get_best_word(letters))
    print(bot.get_evaluated_and_sorted(letters))
