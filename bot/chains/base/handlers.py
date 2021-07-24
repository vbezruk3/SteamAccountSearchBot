from aiogram.types import Message, ContentType

from bot.config import *

from bot.__main__ import bot, dp, steamfunc

import bot.chains.queue.queuefunc as queuefunc

async def init(dp):
    await bot.send_message(chat_id=ADMIN_ID, text = 'Bot started!')

@dp.message_handler(content_types = ContentType.TEXT)
async def search(message: Message):
    #await bot.send_message(chat_id=message.from_user.id, text='wait...')

    flag = False

    lines = []
    lines = message.text.split('\n')

    for link in lines:
        if 'forcedrop.io/user/' in link:
            url = steamfunc.getSteam(link)

            if url != None:


                flag = True

                queuefunc.addLink(url, message.chat.id)
    if flag:
        await bot.send_message(chat_id=message.from_user.id, text='Ок, подождите ...')



