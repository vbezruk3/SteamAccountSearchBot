import time

import asyncio

from bot.config import *

from bot.__main__ import bot

import bot.chains.queue.queuefunc as queuefunc

import bot.chains.steamapi.steamfunc as steamfunc

async def check():
    while True:
        await asyncio.sleep(queue_sleep)

        link = queuefunc.getLink()

        if link == None:
            continue

        url = link[0]

        chat_id = link[1]

        data = steamfunc.getAll(url)

        if data[3] == 'error':
            await bot.send_message(chat_id=chat_id, text=f'Ошибка. Слишком частые запросы. Пауза на {error_sleep} с.')

            await asyncio.sleep(error_sleep)
        else:
            queuefunc.removeLink()

            c = queuefunc.check_sort(chat_id, data)

            await bot.send_message(chat_id=chat_id, text=f'url = {url} cost = {data[3]}, level = {data[0]}, country = {data[2]}, years = {data[1]}, check = {c}')