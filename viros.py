import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests

# cria pasta foto
if not os.path.exists('foto'):
    os.mkdir('foto')
    print(f"The folder 'foto' has been created.")
else:
    print(f"The 'foto' folder already exists.")

# URL of the Wayback Machine archive
archive_url = "https://web.archive.org/web/*/http://www.humor.nl/funnypics/*"

# Create a Firefox WebDriver instance
driver = webdriver.Firefox()
driver.get(archive_url)

#esperando o DOM
time.sleep(4)

def abreLinks():
    # Find all anchor tags (links) on the page
    page_source = driver.page_source #HTML source code
    soup = BeautifulSoup(page_source, "html.parser")
    image_links = [link.get("href") for link in soup.find_all("a") if link.get("href") and link.get("href").endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    for img_url in image_links:
        driver.execute_script("window.open('" + 'https://web.archive.org' + img_url + "','_blank');")

def baixa_imagem(src):
    response = requests.get(src)
    if response.status_code == 200:

        img_name = os.path.basename(src)
        folder = './foto/'

        with open(folder + img_name, 'wb') as file:
            file.write(response.content)
        print("Image downloaded successfully.")

    else:
        print("Failed to download the image.")

def passa_pagina():
    #find and click next page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    botao_next_xpath = "/html/body/div[4]/div[2]/div[2]/div[3]/div[2]/div/ul/li[10]/a"
    botao_next = driver.find_element(By.XPATH, botao_next_xpath)
    botao_next.click()

abreLinks()

time.sleep(4)

# separar imagens puras e baixar
tab_handles = driver.window_handles

for index, tab_handle in enumerate(tab_handles):
    if index == 0:
        continue
    driver.switch_to.window(tab_handle)
    try:
        body = driver.find_element('tag name','body')
        elements_in_body = body.find_elements(By.XPATH, './/*')

        if len(elements_in_body) == 7: #imagem pura
            image = driver.find_element('id','playback')
            src = image.get_attribute('src')
            baixa_imagem(src)
            driver.close()
        else: #calendario
            #search_calendario
            print("calendario")
            driver.close() 
    except: #sem corpo??
        print("sem corpo; url: " + driver.current_url)
        driver.close() 
        pass

driver.switch_to.window(driver.window_handles[0])

passa_pagina()

input('enter')

#separar imagens e calendarios
calendarios = []
imagens = []

'''

for timestamp in timestamp_tries:
    full_url = f"https://web.archive.org/web/{timestamp}/{img_url}"
    driver.get(full_url)

    # Check if the image is available at the current timestamp
    if "This page is available on the web!" in driver.page_source:
        img_data = driver.find_element_by_tag_name("img").screenshot_as_png

        with open(os.path.join(save_directory, img_name), "wb") as f:
            f.write(img_data)

        print(f"Saved {img_name} to {save_directory} at timestamp {timestamp}")
        break
else:
    print(f"Image {img_name} not found at any timestamp")

# Close the WebDriver
driver.quit()

# Add a delay to keep the browser open for inspection
time.sleep(10)  # Wait for 10 seconds

'''