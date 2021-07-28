import time

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

import re

from bs4 import BeautifulSoup

import requests

from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()

prefs = {"profile.managed_default_content_settings.images": 2}

options.add_experimental_option("prefs", prefs)

options.add_argument("disable-popup-blocking")

options.add_argument("disable-infobars")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

url = 'https://csgobackpack.net/index.php?nick=doctortaurus'

driver.get(url)

time.sleep(1)

text = str(driver.page_source)

if 'In total' in text:

    ans = text.find('In total') + 11

    cost = ''

    dollar = 1.18116

    while text[ans] != ' ':
        ans += 1

        cost += text[ans]

    if '€' in cost:
        cost = float(cost.replace('€', '')) * dollar
    else:
        cost = float(cost.replace('$', ''))

    print(cost)