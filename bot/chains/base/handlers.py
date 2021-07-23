from aiogram.types import Message

from bot.config import *

from bot.__main__ import bot, dp, steamfunc

async def init(dp):
    await bot.send_message(chat_id=ADMIN_ID, text = 'Bot started!')

@dp.message_handler(commands=['help'])
async def search_handler(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text='wait...')

    ans = steamfunc.getAll(message.text.replace('/help ', ' '))

    await bot.send_message(chat_id=message.from_user.id, text=f'cost = {ans[3]}, level = {ans[0]}, county = {ans[2]}, years = {ans[1]}')



