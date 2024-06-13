import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


def scrape_page_data():
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'pl')))
    container = driver.find_element(By.CLASS_NAME, 'pl')

    # scroll down to load all content on the page
    for _ in range(4):
        driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(2)

   # skus = container.find_elements(By.CLASS_NAME, 'tooltip-custom')
    prices = container.find_elements(By.CSS_SELECTOR, 'div.prdt-actl-pr')
    description = container.find_elements(By.CSS_SELECTOR, '.titl-cnt.titl.brnd-desc')

    return prices, description


def pagination(url, pages=1):
    prod_num = []
    prod_price = []
    prod_desc = []

    page_num = 0
    # iterate over the pages
    for i in range(1, pages + 1):
        # print(f"this is page {i}")
        driver.get(f"{url}?offset={page_num}")

        prices, description = scrape_page_data()

        for price in prices:
                prod_price.append(price.text)
        for desc in description:
                prod_desc.append(desc.text)
       # print(f"prod_num: {prod_num}")
        print(f"prod_price: {prod_price}")
        print(f"prod_desc: {prod_desc}")
       # print(f"prod_num: {len(prod_num)}")
        print(f"prod_price: {len(prod_price)}")
        print(f"prod_desc: {len(prod_desc)}")

        # increment it by 24 since each page has 24 data
        page_num += 24
        time.sleep(1)

    return prod_price, prod_desc


# set the website URL and initialize the Chrome driver
website = 'https://www.lowes.com/pl/Drywall-tape-reels-Drywall-tools-Drywall-Building-supplies/4294462236'
options = Options()
# options.add_argument("--geolocation=47.8410,-122.2947")  # set geolocation to Lynnwood, WA
driver = uc.Chrome()


# call the pagination function to scrape data and store it in three separate lists
prod_price, prod_desc = pagination(website, pages=1)

# convert the three lists to a pandas dataframe and save it as a CSV file
df = pd.DataFrame({'price': prod_price, 'brand': prod_desc})
df.to_csv('lowesreel.csv', index=False)
print(df)

# quit the Chrome driver
driver.quit()