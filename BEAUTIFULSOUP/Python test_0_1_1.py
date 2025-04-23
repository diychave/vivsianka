import csv
import time
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.bonanza.com/items/search?q[filter_category_id]=3034")

for i in range(3): 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

with open('out_1.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Назва', 'Опис', 'Ціна', 'Фото товару (посилання)', 'Посилання на товар', 'Унікальний ключ', 'Код товару з Bonanza'])


    products = driver.find_elements(By.CSS_SELECTOR, '.search_result_item')

    if products:
        for product in products:
            try:
            
                title = product.find_element(By.CSS_SELECTOR, 'a.item_image_container img').get_attribute("alt")
             
                description = title  
                
            
                price = product.find_element(By.CSS_SELECTOR, '.price').text if product.find_elements(By.CSS_SELECTOR, '.price') else "Цена не указана"

             
                link = product.find_element(By.CSS_SELECTOR, 'a.item_image_container').get_attribute("href")

            
                img_url = product.find_element(By.CSS_SELECTOR, 'a.item_image_container img').get_attribute("src")

              
                unique_key = str(uuid.uuid4())

           
                product_id = product.get_attribute('id').split('-')[1] if product.get_attribute('id') else "Код не найден"

             
                writer.writerow([title, description, price, img_url, link, unique_key, product_id])

            except Exception as e:
                print(f"Ошибка при извлечении данных из товара: {e}")
    else:
        print("Товары не найдены на странице.")

driver.quit()

print("Данные https://www.bonanza.com/items/search?q[filter_category_id]=3034 успешно сохранены в 'out_1.csv'.")



driver = webdriver.Chrome(service=service)


driver.get("https://www.bonanza.com/items/search?q[filter_category_id]=10968")

for i in range(3): 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

with open('out_1.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Назва', 'Опис', 'Ціна', 'Фото товару (посилання)', 'Посилання на товар', 'Унікальний ключ', 'Код товару з Bonanza'])


    products = driver.find_elements(By.CSS_SELECTOR, '.search_result_item')

    if products:
        for product in products:
            try:
            
                title = product.find_element(By.CSS_SELECTOR, 'a.item_image_container img').get_attribute("alt")
             
                description = title  
                
            
                price = product.find_element(By.CSS_SELECTOR, '.price').text if product.find_elements(By.CSS_SELECTOR, '.price') else "Цена не указана"

             
                link = product.find_element(By.CSS_SELECTOR, 'a.item_image_container').get_attribute("href")

            
                img_url = product.find_element(By.CSS_SELECTOR, 'a.item_image_container img').get_attribute("src")

              
                unique_key = str(uuid.uuid4())

           
                product_id = product.get_attribute('id').split('-')[1] if product.get_attribute('id') else "Код не найден"

             
                writer.writerow([title, description, price, img_url, link, unique_key, product_id])

            except Exception as e:
                print(f"Ошибка при извлечении данных из товара: {e}")
    else:
        print("Товары не найдены на странице.")

driver.quit()

print("Данные https://www.bonanza.com/items/search?q[filter_category_id]=10968 успешно сохранены в 'out_1.csv'.")
