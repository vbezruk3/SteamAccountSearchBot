import bot.chains.func.files as files

from bot.config import *

queue = []

chats_id = []

def load():
    global queue, chats_id

    queue = files.loadFile(queue_dir)

    chats_id = files.loadFile(chats_id_dir)

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



