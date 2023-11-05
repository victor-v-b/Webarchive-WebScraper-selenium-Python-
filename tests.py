from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create a Firefox browser instance
driver = webdriver.Firefox()

# Open Google with the initial search term
driver.get("https://www.google.com")

# Perform a search for each number from 1 to 5 in separate tabs
search_terms = ["arabe", "maluco", "assalto", "criança"]

for term in search_terms:
    #js pra abrir aba
    driver.execute_script("window.open('"+f"https://www.google.com/search?q={term}"+"', '_blank');")

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])
    
input('fechar')

for _ in range(len(search_terms)):
    driver.switch_to.window(driver.window_handles[-1])  # Switch to the last tab
    driver.close()  # Close the current tab

driver.switch_to.window(driver.window_handles[0])

print('current url: ' + driver.current_url)

input('enter')
# Close the browser (this will close all tabs)
driver.quit()