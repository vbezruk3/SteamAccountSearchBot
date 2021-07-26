from bot.core import *

import bot.chains.steamapi.steamfunc as steamfunc

import bot.chains.queue.handelrs as queue_handlers

import bot.chains.queue.queuefunc as queuefunc

from aiogram import Bot, Dispatcher, executor, types

def main():
    from bot.chains.base.handlers import dp, init

    dp.loop.create_task(queue_handlers.check())

    executor.start_polling(dp, on_startup = init)

if __name__ == '__main__':
    steamfunc.init()

    queuefunc.load()

    #print(queuefunc.getLink())

    main()
