from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.common.exceptions import NoSuchElementException
from collections import Counter
import csv

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

ordem_dropdown = driver.find_element(By.CLASS_NAME, "andes-dropdown__trigger")
ordem_dropdown.click()

sleep(5)

filtro = driver.find_element(By.XPATH, "//span[text()='Menor preço']")
filtro.click()

sleep(5)

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

ordem_dropdown = driver.find_element(By.CLASS_NAME, "andes-dropdown__trigger")
ordem_dropdown.click()

sleep(5)

filtro = driver.find_element(By.XPATH, "//span[text()='Maior preço']")
filtro.click()

sleep(5)

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

"""
for conteudo in conteudos:
    print(f"Título: {conteudo['titulo']}")
    print(f"Valor: R${conteudo['valor']:.2f}")
    print(f"Link: {conteudo['link']}")
    print("-" * 40)
"""

titulo_counter = Counter(conteudo['titulo'] for conteudo in conteudos)

rank_titulos = titulo_counter.most_common(5)

configuracoes_produtos = []

for titulo, count in rank_titulos:
    link_produto = next((conteudo['link'] for conteudo in conteudos if conteudo['titulo'] == titulo), None)
    driver.get(link_produto)
    sleep(5)

    configuracoes = {}
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody.andes-table__body tr")

    for row in rows:
        key_element = row.find_element(By.TAG_NAME, "th")
        value_element = row.find_element(By.TAG_NAME, "td")
        key = key_element.text.strip()
        value = value_element.text.strip()
        configuracoes[key] = value

    configuracoes_produtos.append({
        "titulo": titulo,
        "configuracoes": configuracoes
    })

"""
print("Configurações dos 5 melhores produtos:")
for produto in configuracoes_produtos:
    print(f"Título: {produto['titulo']}")
    for key, value in produto['configuracoes'].items():
        print(f"{key}: {value}")
    print("-" * 40)
"""

with open('produtos.csv', mode='w+', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Título', 'Características'])

    for produto in configuracoes_produtos:
        caracteristicas = ", ".join([f"{key}: {value}" for key, value in produto['configuracoes'].items()])
        writer.writerow([produto['titulo'], caracteristicas])

sleep(10)
driver.close()
