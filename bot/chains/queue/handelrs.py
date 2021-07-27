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

        if queuefunc.settings[str(link[2])]['stop'] == 'True':
            continue

        url = link[0]

        forcedrop_link = link[1]

        chat_id = link[2]

        data = await steamfunc.getAll(url)

        if data[3] == 'error':
            await bot.send_message(chat_id=chat_id, text=f'Ошибка. Слишком частые запросы. Пауза на {error_sleep} с.')

            await asyncio.sleep(error_sleep)
        else:
            queuefunc.removeLink()

            await bot.send_message(chat_id=chat_id, text=f'Проверка профиля ...')

            await bot.send_message(chat_id=chat_id, text=f"Осталось {len(queuefunc.queue['steam'])}")

            c = queuefunc.check_sort(chat_id, data)

            if data[3] == 'none':
                cost = 'none'
            else:
                cost = round(float(data[3]))

            ans = f'Информация: цена инвентаря: {cost}$, уровень: {data[0]}, лет выслуги: {data[1]}, регион: {data[2]}'

            if c == False:
                ans += ' Не подходит('
            else:
                ans += ' Подходит!'

            await bot.send_message(chat_id=chat_id, text=ans)

            if c == True:
                queuefunc.addResult(chat_id, data, url, forcedrop_link)