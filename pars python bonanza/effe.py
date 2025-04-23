from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Настроим Selenium для работы с Chrome
driver = webdriver.Chrome(ChromeDriverManager().install())

# URL страницы Bonanza
url = "https://www.bonanza.com/items/search?q[filter_category_id]=10968"

# Открываем страницу
driver.get(url)

# Используем явное ожидание для того, чтобы дождаться появления товаров
try:
    # Ждем, пока хотя бы один товар не появится на странице
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'item_card'))
    )

    # Находим все товары на странице
    products = driver.find_elements(By.CLASS_NAME, 'item_card')

    if products:
        for product in products:
            try:
                # Извлекаем название и цену товара
                title = product.find_element(By.CLASS_NAME, 'title')
                price = product.find_element(By.CLASS_NAME, 'price')

                print(f"Название товара: {title.text}")
                print(f"Цена товара: {price.text}")
                print('---')
            except Exception as e:
                print(f"Ошибка при извлечении данных из товара: {e}")

    else:
        print("Товары не найдены на странице.")
except Exception as e:
    print(f"Ошибка при загрузке страницы: {e}")
finally:
    # Закрываем браузер
    driver.quit()
