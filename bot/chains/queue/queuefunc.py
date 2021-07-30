import bot.chains.func.files as files

from bot.config import *

import re

import bot.chains.steamapi.steamfunc as steamfunc

from bot.__main__ import bot

queue = {}

chats_id = []

sites = []

settings = {}

stats = {}

results = {}

def isBetween(value, intrv, incl):
    if (value > intrv[0] or (incl[0] == 'True' and value == intrv[0])) and (value < intrv[1] or (incl[1] == 'True'and value == intrv[1])):
        return True
    return False

def check_sort(chat_id, data):
    setting = settings[str(chat_id)]

    level_intrvl = [float(setting["level"]["intrv"][0] - setting["level"]["intrv"][0] * setting["level"]["mist"]), float(setting["level"]["intrv"][1] + setting["level"]["intrv"][1] * setting["level"]["mist"])]

    cost_intrvl = [float(setting["cost"]["intrv"][0] - setting["cost"]["intrv"][0] * setting["cost"]["mist"]), float(setting["cost"]["intrv"][1] + setting["cost"]["intrv"][1] * setting["cost"]["mist"])]

    rank_intrvl = [float(setting["rank"]["intrv"][0] - setting["rank"]["intrv"][0] * setting["rank"]["mist"]), float(setting["rank"]["intrv"][1] + setting["rank"]["intrv"][1] * setting["rank"]["mist"])]

    if data[0] == 'none':
        level = 'none'
    else:
        level = float(data[0])

    county = data[2]

    if data[3] == 'none':
        return False

    if data[1] == 'none':
        rank = 'none'
    else:
        rank = float(data[1])

    cost = data[3]

    #print(cost)

    #print(cost_intrvl)

    if not (county in setting["country"] or county == 'none'):
        return False

    if not (level == 'none' or isBetween(level, level_intrvl, setting["level"]["incl"])):
        return False

    if not (rank == 'none' or isBetween(rank, rank_intrvl, setting["rank"]["incl"])):
        return False

    if not isBetween(cost, cost_intrvl, setting["cost"]["incl"]):
        return False

    return True

def load():
    global queue, chats_id, settings, results, sites, stats

    queue = files.loadFile(queue_dir)

    chats_id = files.loadFile(chats_id_dir)

    settings = files.loadFile(settings_dir)

    results = files.loadFile(results_dir)

    sites = files.loadFile(sites_dir)

    stats = files.loadFile(stats_dir)

def getLink():
    if not queue["steam"]:
        return None

    return [queue["steam"][0], queue["forcedrop"][0], str(chats_id[0])]

def removeLink():
    queue["steam"].pop(0)
    queue["forcedrop"].pop(0)

    chats_id.pop(0)

    save()

    return

def addLink(url, link, chat_id):

    if link not in sites:
        queue['steam'].append(url)
        queue['forcedrop'].append(link)

        chats_id.append(chat_id)

        sites.append(link)

        save()

    return

def checkUser(chat_id):
    if str(chat_id) not in settings.keys():
        return False
    return True

def addUser(chat_id):
    setting = settings['default']

    settings[str(chat_id)] = setting

    results[str(chat_id)] = []

    save()

def getParams(param):
    nums = re.findall(r'\d+', param)

    nums = [int(i) for i in nums]

    return nums

def changeSettings(chat_id, param):

    if 'цена инвентаря ' in param:
        param = param.replace('цена инвентаря ', '')

        nums = getParams(param)

        settings[str(chat_id)]['cost']['intrv'][0] = nums[0]
        settings[str(chat_id)]['cost']['intrv'][1] = nums[1]
        settings[str(chat_id)]['cost']["mist"] = float(nums[2] / 100)

        if '[' in param:
            settings[str(chat_id)]['cost']["incl"][0] = 'True'
        else:
            settings[str(chat_id)]['cost']["incl"][0] = 'False'

        if ']' in param:
            settings[str(chat_id)]['cost']["incl"][1] = 'True'
        else:
            settings[str(chat_id)]['cost']["incl"][1] = 'False'

        save()

        return 'Цена инвентаря изменена'

    if 'уровень ' in param:
        param = param.replace('уровень ', '')

        nums = getParams(param)

        settings[str(chat_id)]['level']['intrv'][0] = nums[0]
        settings[str(chat_id)]['level']['intrv'][1] = nums[1]
        settings[str(chat_id)]['level']["mist"] = float(nums[2] / 100)

        if '[' in param:
            settings[str(chat_id)]['level']["incl"][0] = 'True'
        else:
            settings[str(chat_id)]['level']["incl"][0] = 'False'

        if ']' in param:
            settings[str(chat_id)]['level']["incl"][1] = 'True'
        else:
            settings[str(chat_id)]['level']["incl"][1] = 'False'

        save()

        return 'Уровень изменен'

    if 'лет выслуги ' in param:
        param = param.replace('лет выслуги ', '')

        nums = getParams(param)

        settings[str(chat_id)]['rank']['intrv'][0] = nums[0]
        settings[str(chat_id)]['rank']['intrv'][1] = nums[1]
        settings[str(chat_id)]['rank']["mist"] = float(nums[2] / 100)

        if '[' in param:
            settings[str(chat_id)]['rank']["incl"][0] = 'True'
        else:
            settings[str(chat_id)]['rank']["incl"][0] = 'False'

        if ']' in param:
            settings[str(chat_id)]['rank']["incl"][1] = 'True'
        else:
            settings[str(chat_id)]['rank']["incl"][1] = 'False'

        save()

        return 'Лет выслуги изменено'

    if 'регионы ' in param:
        param = param.replace('регионы ', '')

        if 'добавить ' in param:
            param = param.replace('добавить ', '')

            if param not in steamfunc.countries:
                return 'Нет такого региона'

            settings[str(chat_id)]['country'].append(param)

            save()

            return 'Регион добавлен'

        if 'удалить ' in param:
            param = param.replace('удалить ', '')

            if param not in settings[str(chat_id)]['country']:
                return 'Такой регион не добавлен у вас'

            settings[str(chat_id)]['country'].remove(param)

            save()

            return 'Регион удален'

    return 'Ошибка'

async def sendResult(chat_id):
    count = len(results[str(chat_id)])

    if count == 0:
        await bot.send_message(chat_id=chat_id, text=f'Нету найденых аккаунтов')

        return

    f = open('result.txt', 'w')

    ans = f'Naideno {count} accauntov:\n'

    for result in results[str(chat_id)]:
        ans += result + '\n'

    results[str(chat_id)] = []

    save()

    f.write(ans)

    f.close()

    await bot.send_document(chat_id=chat_id, document=open('result.txt', 'rb'))

def addResult(chat_id, result, steam_url, forcedrop_url):

    #res = str(result[0]) + ' ' + str(result[1]) + ' ' + str(result[2]) + ' ' + str(result[3]) + ' ' + steam_url + ' ' + forcedrop_url

    res = f'Steam: {steam_url}, Site: {forcedrop_url}, cena inventarya: {round(float(result[3]))}$, uroven: {result[0]}, let vislugi: {result[1]}, region: {result[2]}'

    results[str(chat_id)].append(res)

    save()

def getSettings(chat_id):
    setting = settings[str(chat_id)]

    ans = 'Ваши настройки отбора:\n'

    ans += '\t -цена инвентаря: '

    if setting["cost"]["incl"][0] == 'True':
        ans += '['
    else:
        ans += '('

    ans += f'{setting["cost"]["intrv"][0]}; {setting["cost"]["intrv"][1]}'

    if setting["cost"]["incl"][1] == 'True':
        ans += ']'
    else:
        ans += ')'

    ans += f' +- {float(setting["cost"]["mist"]) * 100}%\n'

    #

    ans += '\t -уровень: '

    if setting["level"]["incl"][0] == 'True':
        ans += '['
    else:
        ans += '('

    ans += f'{setting["level"]["intrv"][0]}; {setting["level"]["intrv"][1]}'

    if setting["level"]["incl"][1] == 'True':
        ans += ']'
    else:
        ans += ')'

    ans += f' +- {float(setting["level"]["mist"]) * 100}%\n'

    #

    ans += '\t -лет выслуги: '

    if setting["rank"]["incl"][0] == 'True':
        ans += '['
    else:
        ans += '('

    ans += f'{setting["rank"]["intrv"][0]}; {setting["rank"]["intrv"][1]}'

    if setting["rank"]["incl"][1] == 'True':
        ans += ']'
    else:
        ans += ')'

    ans += f' +- {float(setting["rank"]["mist"]) * 100}%\n'

    ans += f'\t -регионы: {setting["country"]}'

    return ans

def save():
    files.saveFile(queue, queue_dir)

    files.saveFile(chats_id, chats_id_dir)

    files.saveFile(settings, settings_dir)

    files.saveFile(results, results_dir)

    files.saveFile(sites, sites_dir)

    files.saveFile(stats, stats_dir)

