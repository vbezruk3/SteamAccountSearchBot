import os

from selenium import webdriver

TELEGRAM_BOT_TOKEN = '1867495675:AAFEUY4sqCdfbv-2OSm0pMA-TFW9C9ULlxI'

ADMIN_ID = '671836800'

extension_dir = './../extensions/Steam-Inventory-Helper.crx'

countries_dir = './../data/countries.json'

queue_dir = './../data/queue.json'

chats_id_dir = './../data/chats_id.json'

settings_dir = './../data/sort_settings.json'

results_dir = './../data/results.json'

options = webdriver.ChromeOptions()

prefs = {"profile.managed_default_content_settings.images": 2}

options.add_experimental_option("prefs", prefs)

options.add_extension(extension_dir)

options.add_argument("disable-popup-blocking")

options.add_argument("disable-infobars")

queue_sleep = 45

error_sleep = 90

sleep_time1 = 1

sleep_time2 = 3

forcedrop_time = 3


