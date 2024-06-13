from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time
import pandas as pd


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

website = 'https://www.grainger.com/search/tools/hand-tools/drywall-plastering-tools/putty-knives-scrapers?ts_optout=true&searchQuery=drywall&categoryIndex=2'
driver.get(website)

tables = driver.find_elements(By.XPATH, '//tbody[@class="cjpIYY"]')
prod_num = []
prod_price = []
prod_desc = []
for i in range(len(tables)):
    table = driver.find_elements(By.XPATH, '//tbody[@class="cjpIYY"]')[i]
    rows = table.find_elements(By.CLASS_NAME, '-dql2z')
    j = 0
    for j in range(len(rows)):
        # update references
        table = driver.find_elements(By.XPATH, '//tbody[@class="cjpIYY"]')[i]
        row = table.find_elements(By.CLASS_NAME, '-dql2z')[j]

        row.click()
        # to load the expanded information of the row
        time.sleep(2)
        # product page link
        product_page = driver.find_element(By.XPATH, '//a[@class="JEyT-B _3ihaM4"]')
        product_page.click()
        time.sleep(3)

        # Extract data
        product = driver.find_element(By.XPATH, '//div[@class="vDgTDH"][2]/dd')
       # price = driver.find_element(By.XPATH, '//span[@class="rbqU0E lVwVq5"]')
        #clear_price = driver.find_element(By.XPATH, '//span[@class="rbqU0E pGN3Jf lVwVq5"]')
        description = driver.find_element(By.XPATH, '//h1[@class="lypQpT"]')
        try:
            price = driver.find_element(By.XPATH, '//span[@class="rbqU0E lVwVq5"]')
            prod_price.append(price.text)
            print("Price: %s" % driver.find_element(By.XPATH, '//span[@class="rbqU0E lVwVq5"]').text)
        except NoSuchElementException:
            clear_price = driver.find_element(By.XPATH, '//span[@class="rbqU0E pGN3Jf lVwVq5"]')
            prod_price.append(clear_price.text)
            print("Price: %s" % driver.find_element(By.XPATH, '//span[@class="rbqU0E pGN3Jf lVwVq5"]').text)
        prod_num.append(product.text)
       # prod_price.append(price.text)
        prod_desc.append(description.text)
        print("Mfr. model: %s" % driver.find_element(By.XPATH, '//div[@class="vDgTDH"][2]/dd').text)
        #print("Price: %s" % driver.find_element(By.XPATH, '//span[@class="rbqU0E lVwVq5"]').text)
        print("Description: %s" % driver.find_element(By.XPATH, '//h1[@class="lypQpT"]').text)

        driver.back()
        print()
        j += 1
    print()
    i += 1
df = pd.DataFrame({'code': prod_num, 'price': prod_price, 'brand': prod_desc})
df.to_csv('octgrainknives.csv', index=False)
print(df)
driver.quit()
