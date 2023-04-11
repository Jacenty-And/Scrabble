from random import choice
from threading import Thread, Event
from time import time, sleep
from bs4 import BeautifulSoup
from requests import get
from concurrent.futures import ThreadPoolExecutor


def get_soup_init(url, print_response=True) -> BeautifulSoup:
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"
    ]
    random_user_agent = choice(user_agents)
    headers = {'User-Agent': random_user_agent}
    request = get(url, headers=headers)
    max_attempts = 5
    attempts = 0
    while request.status_code != 200:
        request = get(url, headers=headers)
        attempts += 1
        if attempts == max_attempts and request.status_code != 200:
            if print_response:
                start_index = url.find("id=")
                end_index = url.find("-literowe")
                length = url[start_index + len("id="):end_index]
                start_index = url.find("litere-")
                letter = url[start_index + len("litere-")]
                print(f'\nLetter: {letter} length: {length}: {request}')
            break
    html_text = request.text
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup


def save_to_file(all_words, name, path):
    with open(f'{path}{name}.txt', 'w', encoding='UTF8') as txt_file:
        for words in all_words:
            for word in words:
                txt_file.write(word + ' ')
            txt_file.write('\n')


def get_words(url) -> list:
    soup = get_soup_init(url)
    divs = soup.find_all('div', class_='card-wrapper')
    words = list()
    for div in divs:
        words.extend(div.find('p').text
                     .replace('.', '')
                     .replace(',', ' ')
                     .split())
    return words


def get_urls(alphabet) -> list:
    urls = list()
    for letter in alphabet:
        for length in range(2, 16):
            url = f"https://polski-slownik.pl/wszystkie-slowa-jezyka-polskiego.php" \
                  f"?id={length}-literowe-na-litere-{letter}" \
                  f"&Submit=CHCĘ+WSZYSTKIE+SŁOWA"
            urls.append(url)
    return urls


class Timer(Thread):
    def __init__(self):
        super(Timer, self).__init__()
        self._event = Event()
        self._start = 0

    def run(self):
        self._start = time()
        while not self._event.is_set():
            print(f"\rTime: {round(time() - self._start, 2)} s", end='')
            sleep(0.1)

    def stop(self):
        self._event.set()
        print(f" = ~{round((time() - self._start) / 60, 1)} minutes")


class Scraper:
    def __init__(self):
        self.alphabet = 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż'

    def run(self, file_name='words', file_path=''):
        print("Scraping...")
        timer = Timer()
        timer.start()
        urls = get_urls(self.alphabet)
        with ThreadPoolExecutor() as executor:
            all_words = list(executor.map(get_words, urls))
        save_to_file(all_words, file_name, file_path)
        timer.stop()
        print(f"{sum([len(words) for words in all_words]):,} words saved: {file_path}{file_name}.txt")
        return all_words

    def run_no_threading(self, file_name='words', file_path=''):
        print("Scraping without threading...")
        timer = Timer()
        timer.start()
        all_words = list()
        urls = get_urls(self.alphabet)
        for url in urls:
            words = get_words(url)
            all_words.append(words)
        save_to_file(all_words, file_name, file_path)
        timer.stop()
        print(f"{sum([len(words) for words in all_words]):,} words saved: {file_path}{file_name}.txt")
        return all_words
