from aiogram.types import Message

from bot.config import *

from bot.__main__ import bot, dp, steamfunc

import bot.chains.queue.queuefunc as queuefunc

async def init(dp):
    await bot.send_message(chat_id=ADMIN_ID, text = 'Bot started!')

@dp.message_handler(commands=['help'])
async def search_handler(message: Message):
    #await bot.send_message(chat_id=message.from_user.id, text='wait...')

    queuefunc.addLink(message.text.replace('/help ', ''), message.chat.id)

    await bot.send_message(chat_id=message.from_user.id, text='Ok, wait ...')



