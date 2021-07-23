import time

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

import re

from bs4 import BeautifulSoup

import requests

from webdriver_manager.chrome import ChromeDriverManager

def init():
    global driver

    options = webdriver.ChromeOptions()

    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    options.add_extension('./Steam-Inventory-Helper_v1.17.70.crx')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

def getId(url):
    url = f'{url}/?xml=1'

    r = requests.get(url)

    soup = BeautifulSoup(r.text, features="html.parser")

    tables = str(soup.find_all('steamid64'))[12:].replace('</steamid64>]', '')

    return tables

def getInf(id):
    url = f'https://steamid.pro/lookup/{id}'

    r = requests.get(url)

    soup = BeautifulSoup(r.text, features="html.parser")

    tables = str(soup.find_all('ul', {'class': 'player-info'}))

    #print(tables)

    lk = tables.find('Level <span>')
    k = 0

    level = ''

    while tables[lk + 12 + k] != '<':
        level += tables[lk + 12 + k]

        k += 1

    #print(level)

    rk = tables.find('"number" title="">')
    k = 0

    rank = ''

    while tables[rk + 18 + k] != '<':
        rank += tables[rk + 18 + k]

        k += 1

    #print(rank)

    ck = tables.find('flag-icon-') + 10

    k = 0

    country = ''

    while tables[ck + k] != '"':
        country += tables[ck + k]

        k += 1

    #print(country)

    return [level, rank, country]

def getCost(url):

    url = f'{url}/inventory/#730'

    driver.get(url)

    time.sleep(1)

    element = driver.find_element_by_id("invValue")

    element.click()

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source)
    tables = str(soup.find_all('span', {'class': 'priceValue'})[1])[26:].replace('</span>', '')

    return tables

def getAll(url):
    cost = getCost(url)
    id = getId(url)
    inf = getInf(id)

    inf.append(cost)

    return inf

init()

print(getAll('https://steamcommunity.com/id/VladSukr'))

time.sleep(2)

print(getAll('https://steamcommunity.com/id/aveAMERICA'))




