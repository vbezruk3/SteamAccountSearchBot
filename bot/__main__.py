from bot.core import *

import bot.chains.steamapi.steamfunc as steamfunc

def main():
    from bot.chains.base.handlers import dp, init
    executor.start_polling(dp, on_startup = init)

if __name__ == '__main__':
    steamfunc.init()
    main()
