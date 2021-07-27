from aiogram.types import Message, ContentType

from bot.config import *

from bot.__main__ import bot, dp, steamfunc

import bot.chains.queue.queuefunc as queuefunc

import time

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

import re

from bs4 import BeautifulSoup

import requests

from webdriver_manager.chrome import ChromeDriverManager

import bot.chains.func.files as files

async def init(dp):
    global driverforce

    driverforce = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    await bot.send_message(chat_id=ADMIN_ID, text = 'Bot started!')

@dp.message_handler(commands=['результат'])
async def search(message: Message):

    await queuefunc.sendResult(message.chat.id)

    return

@dp.message_handler(commands=['помощь'])
async def search(message: Message):
    if queuefunc.checkUser(message.chat.id) == False:
        queuefunc.addUser(message.chat.id)

    answer = 'Команды:\n'

    answer += '/статус - сколько найдено аккаунтов\n'
    answer += '/настройки - Ваши настройки\n'
    answer += '/результат - получить файл с найденными аккаунтами, если они есть\n'

    await bot.send_message(chat_id=message.from_user.id, text=answer)

    return

@dp.message_handler(commands=['настроить'])
async def search(message: Message):

    #цена инвентаря

    command = message.text.replace('/настроить ', '')

    await bot.send_message(chat_id=message.from_user.id, text=queuefunc.changeSettings(message.chat.id, command))

    return

@dp.message_handler(commands=['статус'])
async def search(message: Message):
    if queuefunc.checkUser(message.chat.id) == False:
        queuefunc.addUser(message.chat.id)

    if queuefunc.settings[str(message.chat.id)]["stop"] == 'False':
        ans_w = 'да'
    else:
        ans_w = 'нет'

    answer = f'Бот работает: {ans_w}\n'
    answer += f'Найдено профилей: {len(queuefunc.results[str(message.chat.id)])}'

    await bot.send_message(chat_id=message.from_user.id, text=answer)

@dp.message_handler(commands=['настройки'])
async def search(message: Message):
    if queuefunc.checkUser(message.chat.id) == False:
        queuefunc.addUser(message.chat.id)

    await bot.send_message(chat_id=message.from_user.id, text=queuefunc.getSettings(message.chat.id))

async def getSteam(url):
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

@dp.message_handler(content_types = ContentType.TEXT)
async def search(message: Message):

    if queuefunc.checkUser(message.chat.id) == False:
        queuefunc.addUser(message.chat.id)

    flag = False

    lines = []
    lines = message.text.split('\n')

    count = len(lines)

    i = 0

    if 'forcedrop' in message.text:
        await bot.send_message(chat_id=message.from_user.id, text='Профили добавляются')

    for link in lines:
        if 'forcedrop' in link:
            i += 1

            url = await getSteam(link)

            if url != None:


                flag = True

                queuefunc.addLink(url, link, message.chat.id)

            if i % 10 == 0:
                await bot.send_message(chat_id=message.from_user.id, text=f'Добавлено {i} из {count}')

    if flag == True:
        await bot.send_message(chat_id=message.from_user.id, text='Профили добавлены')

