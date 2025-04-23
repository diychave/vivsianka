import requests
from bs4 import BeautifulSoup

# URL страницы Bonanza, с которой будем парсить данные
url = "https://www.bonanza.com/items/search?q[filter_category_id]=10968"

# Отправка GET-запроса на страницу
response = requests.get(url)

# Проверка, успешен ли запрос
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем все товары на странице (попробуем найти контейнеры с товарами)
    products = soup.find_all('div', class_='item_card')

    for product in products:
        # Извлекаем название товара
        title = product.find('span', class_='title')
        # Извлекаем цену товара
        price = product.find('span', class_='price')

        # Если элементы найдены, выводим информацию
        if title and price:
            print(f"Название товара: {title.get_text()}")
            print(f"Цена товара: {price.get_text()}")
            print('---')
else:
    print(f"Не удалось загрузить страницу, статус: {response.status_code}")
