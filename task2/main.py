import sys
from collections import Counter
import requests
from bs4 import BeautifulSoup
import csv

# Стартовый URL для парсинга
URL = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
# Список для сбора букв
alphabet = []

def wikiAnimalsParsing(URL):
    # Скачиваем HTML содержимое
    contents = requests.get(URL).text
    # Парсим содержимое
    soup = BeautifulSoup(contents, 'html.parser')
    # Берем основной div, в котором находится нужный список
    content_div = soup.find('div', attrs={'class': 'mw-category-columns'})

    # Итерируемся по каждому нужному нам элементу li
    for raw in content_div.select('li'):
        # Берем первую букву из текста ссылки в каждом нужном нам элементе
        first_letter = raw.a.text[0]
        # Указываем, когда нужно остановиться - когда увидим английскую букву A
        if first_letter == 'A':
            # Методом счетчика получаем количество каждой буквы в нашем списке для сбора букв
            count = Counter(alphabet)
            # Сортируем элементы и кладем их как список в новый словарь
            sorted_alphabet = dict(sorted(count.items()))
            # Сохраняем результаты в файл CSV
            save_to_csv(sorted_alphabet)
            # Выходим из программы, если выполнено условие останова
            sys.exit()
        else:
            # Если условие останова не выполнено, то первую букву из текста ссылки добавляем в список для сбора букв
            alphabet.append(first_letter)
    # Берем со страницы URL, который находится в элементе с текстом Следующая страница
    next_url = soup.find('a', text='Следующая страница')
    # Запускаем эту же функцию со следующим URL
    wikiAnimalsParsing("https://ru.wikipedia.org" + next_url.get('href'))

def save_to_csv(data, filename="beasts.csv"):
    """Сохраняем результаты подсчёта в CSV-файл."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Записываем данные: каждая буква и количество
        for letter, count in data.items():
            writer.writerow([letter, count])

# Запускаем парсинг
wikiAnimalsParsing(URL)
