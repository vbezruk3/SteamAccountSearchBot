import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.config import *

bot = Bot(TELEGRAM_BOT_TOKEN, parse_mode = 'HTML')

dp = Dispatcher(bot, storage = MemoryStorage(), loop = asyncio.get_event_loop())
