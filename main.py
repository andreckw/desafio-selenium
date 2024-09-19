from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.common.exceptions import NoSuchElementException

from time import sleep

driver = webdriver.Chrome()
driver.get("https://www.mercadolivre.com.br/")

sleep(5)

input1 = driver.find_element(By.ID, "cb1-edit")
input1.send_keys("cabo")
input1.send_keys(Keys.ENTER)

sleep(5)


conteudos = []

for i in range(2):
    conteudos_page = driver.find_elements(By.CLASS_NAME, "ui-search-layout__item")

    for cont in conteudos_page:
        titulo_element = cont.find_element(By.TAG_NAME, "h2")
        titulo = titulo_element.text
        real = cont.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text.replace('.', '')
        try:
            cent_element = cont.find_element(By.CLASS_NAME, "andes-money-amount__cents")
            cents = cent_element.text
        except NoSuchElementException:
            cents = 0

        valor = float(f'{real}.{cents}')
        link = cont.find_element(By.TAG_NAME, "a").get_attribute("href")

        conteudos.append({
            "titulo": titulo,
            "valor": valor,
            "link": link
        })

    btn = driver.find_element(By.CLASS_NAME, 'andes-pagination__button--next')
    btn = btn.find_element(By.TAG_NAME, 'a')
    btn.send_keys(Keys.ENTER)
    sleep(5)


sleep(10)
driver.close()


