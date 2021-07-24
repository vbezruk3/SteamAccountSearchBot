import bot.chains.func.files as files

from bot.config import *

queue = []

chats_id = []

settings = {}

def check_sort(chat_id, data):
    setting = settings['default']

    setting["level"]["intrv"][0] -= setting["level"]["intrv"][0] * setting["level"]["mist"]

    setting["level"]["intrv"][0] = float(setting["level"]["intrv"][0])

    setting["cost"]["intrv"][0] -= setting["cost"]["intrv"][0] * setting["cost"]["mist"]

    setting["cost"]["intrv"][0] = float(setting["cost"]["intrv"][0])

    setting["rank"]["intrv"][0] -= setting["rank"]["intrv"][0] * setting["rank"]["mist"]

    setting["rank"]["intrv"][0] = float(setting["rank"]["intrv"][0])


    setting["level"]["intrv"][1] += setting["level"]["intrv"][1] * setting["level"]["mist"]

    setting["level"]["intrv"][1] = float(setting["level"]["intrv"][1])

    setting["cost"]["intrv"][1] += setting["cost"]["intrv"][1] * setting["cost"]["mist"]

    setting["cost"]["intrv"][1] = float(setting["cost"]["intrv"][1])

    setting["rank"]["intrv"][1] += setting["rank"]["intrv"][1] * setting["rank"]["mist"]

    setting["rank"]["intrv"][1] = float(setting["rank"]["intrv"][1])

    level = float(data[0])
    rank = float(data[1])
    county = data[2]
    cost = float(data[3])

    if not (county in setting["country"] or county == 'none'):
        return False

    if not ((level > setting["level"]["intrv"][0] or (setting["level"]["incl"][0] and level == setting["level"]["intrv"][0])) and
        (level < setting["level"]["intrv"][1] or (setting["level"]["incl"][1] and level == setting["level"]["intrv"][1]))):
        return False

    if not ((rank > setting["rank"]["intrv"][0] or (setting["rank"]["incl"][0] and rank == setting["rank"]["intrv"][0])) and
        (rank < setting["rank"]["intrv"][1] or (setting["rank"]["incl"][1] and rank == setting["rank"]["intrv"][1]))):
        return False

    if not ((cost == 'none' or cost > setting["cost"]["intrv"][0] or (setting["cost"]["incl"][0] and cost == setting["cost"]["intrv"][0])) and
        (cost < setting["cost"]["intrv"][1] or (setting["cost"]["incl"][1] and cost == setting["cost"]["intrv"][1]))):
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