import bot.chains.func.files as files

from bot.config import *

queue = []

chats_id = []

settings = {}

def isBetween(value, intrv, incl):
    if (value > intrv[0] or (incl[0] and value == intrv[0])) and (value < intrv[1] or (incl[1] and value == intrv[1])):
        return True
    return False

def check_sort(chat_id, data):
    setting = settings['default']

    level_intrvl = [float(setting["level"]["intrv"][0] - setting["level"]["intrv"][0] * setting["level"]["mist"]), float(setting["level"]["intrv"][1] + setting["level"]["intrv"][1] * setting["level"]["mist"])]

    cost_intrvl = [float(setting["cost"]["intrv"][0] - setting["cost"]["intrv"][0] * setting["cost"]["mist"]), float(setting["cost"]["intrv"][1] + setting["cost"]["intrv"][1] * setting["cost"]["mist"])]

    rank_intrvl = [float(setting["rank"]["intrv"][0] - setting["rank"]["intrv"][0] * setting["rank"]["mist"]), float(setting["rank"]["intrv"][1] + setting["rank"]["intrv"][1] * setting["rank"]["mist"])]

    level = float(data[0])
    rank = float(data[1])
    county = data[2]

    if data[3] != 'none':
        cost = float(data[3])
    else:
        cost = 'none'

    if not (county in setting["country"] or county == 'none'):
        return False

    if not isBetween(level, level_intrvl, setting["level"]["incl"]):
        return False

    if not isBetween(rank, rank_intrvl, setting["rank"]["incl"]):
        return False

    if cost != 'none':
        if not isBetween(cost, cost_intrvl, setting["cost"]["incl"]):
            return False

    return True

def load():
    global queue, chats_id, settings

    queue = files.loadFile(queue_dir)

    chats_id = files.loadFile(chats_id_dir)

    settings = files.loadFile(settings_dir)

def getLink():
    if not queue:
        return None

    return [queue[0], chats_id[0]]

def removeLink():
    queue.pop(0)

    chats_id.pop(0)

    save()

    return

def addLink(url, chat_id):
    queue.append(url)

    chats_id.append(chat_id)

    save()

    return

def save():
    files.saveFile(queue, queue_dir)

    files.saveFile(chats_id, chats_id_dir)

    files.saveFile(settings, settings_dir)