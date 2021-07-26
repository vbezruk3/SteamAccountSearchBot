import time

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

import re

from bs4 import BeautifulSoup

import requests

from webdriver_manager.chrome import ChromeDriverManager

from bot.config import *

import bot.chains.func.files as files

countries = []

def init():
    global driver, countries, driverforce

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driverforce = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    countries = files.loadFile(countries_dir)

def getSteam(url):
    driverforce.get(url)

    time.sleep(forcedrop_time)

    soup = BeautifulSoup(driverforce.page_source, features="html.parser")

    try:
        element = driverforce.find_element_by_class_name("profile-main__steam")
    except:
        return None

    tables = str(soup.find_all('a', {'class': 'profile-main__steam'}))

    url = ''

    k = 0

    i = tables.find('href="') + 6

    while tables[k + i] != '"':
        url += tables[k + i]

        k += 1

    return url

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

    lk = tables.find('Level <span>')
    k = 0

    level = ''

    while tables[lk + 12 + k] != '<':
        level += tables[lk + 12 + k]

        k += 1

    rk = tables.find('"number" title="">')
    k = 0

    rank = ''

    while tables[rk + 18 + k] != 'y':
        rank += tables[rk + 18 + k]

        k += 1

    ck = tables.find('flag-icon-') + 10

    k = 0

    country = ''

    while tables[ck + k] != '"':
        country += tables[ck + k]

        k += 1

    if country not in countries:
        country = 'none'

    return [level, rank, country]

def getCost(url):

    url = f'{url}/inventory/#730'

    driver.get(url)

    time.sleep(sleep_time1)

    try:
        element = driver.find_element_by_class_name("error_ctn")

        return 'error'
    except:
        pass

    try:
        element = driver.find_element_by_id("invValue")
    except:
        return 'none'

    element.click()

    time.sleep(sleep_time2)

    soup = BeautifulSoup(driver.page_source, features="html.parser")
    tables = str(soup.find_all('span', {'class': 'priceValue'})[1])[26:].replace('</span>', '')

    tables = float(tables.replace(',', ''))

    return tables

def getAll(url):
    cost = getCost(url)
    id = getId(url)
    inf = getInf(id)

    inf.append(cost)

    return inf




