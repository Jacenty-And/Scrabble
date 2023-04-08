from time import time
from bs4 import BeautifulSoup
from requests import get
from concurrent.futures import ThreadPoolExecutor


def get_soup_init(url, print_response=False):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"}
    request = get(url, headers=headers)
    if print_response:
        print(f'{request}: {url}')
    html_text = request.text
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup


def save_to_file(all_words, name, path):
    with open(f'{path}{name}.txt', 'w', encoding='UTF8') as txt_file:
        for words in all_words:
            for word in words:
                txt_file.write(word + ' ')
            txt_file.write('\n')


def get_words(url):
    soup = get_soup_init(url)
    divs = soup.find_all('div', class_='card-wrapper')
    words = list()
    for div in divs:
        words.extend(div.find('p').text
                     .replace('.', '')
                     .replace(',', ' ')
                     .split())
    return words


def get_urls(alphabet):
    urls = list()
    for letter in alphabet:
        for length in range(2, 16):
            url = f"https://polski-slownik.pl/wszystkie-slowa-jezyka-polskiego.php" \
                  f"?id={length}-literowe-na-litere-{letter}" \
                  f"&Submit=CHCĘ+WSZYSTKIE+SŁOWA"
            urls.append(url)
    return urls


class Scraper:
    def __init__(self):
        self.alphabet = 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż'

    def run(self, file_name='words', file_path=''):
        print("Scraping...")
        start = time()
        urls = get_urls(self.alphabet)
        with ThreadPoolExecutor() as executor:
            all_words = list(executor.map(get_words, urls))
        save_to_file(all_words, file_name, file_path)
        end = time()
        print(f"Time: ~{round((end - start)/60, 1)} minutes")
        print(f"{sum([len(words) for words in all_words]):,} words saved: {file_path}{file_name}.txt")
        return all_words
