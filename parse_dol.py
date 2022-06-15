import requests
from bs4 import BeautifulSoup


def convert_dol_rub():
    url = 'https://www.cbr.ru/'
    response = requests.get(url)  # get-запрос
    soup = BeautifulSoup(response.text, 'lxml')  # считывание
    # Поиск текущего курса доллара к рублю
    rub = soup.find('div', class_='col-md-2 col-xs-9 _right mono-num').text.strip(' ₽\r\n\t').replace(',', '.')
    return float(rub)
