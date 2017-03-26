import vk_requests
import requests
import json
from shutil import move
import saver
from vk_polling import VKPooler
from vk_polling.VKPooler import Codes
import msce_getter as msce
import sender
import random

app_id = 5037590

permissions = ['offline', 'messages', 'docs']

def getSettings():
    try:
        with open('actions.json', encoding='UTF-8') as data_file:
            data = json.load(data_file)
            return data
    except ValueError:
        return None
    except Exception as ex:
        print(ex.__str__())




def saveDoc(api, update):
    if len(update) > 7:
        for i in range(1, 11):
            if 'attach{}_type'.format(str(i)) in update[7]:
                if update[7]['attach{}_type'.format(str(i))] == 'doc':
                    resp = api.docs.getById(docs=update[7]['attach{}'.format(str(i))])
                    r = requests.get(resp[0]['url'], stream=True)
                    if r.status_code == 200:
                        move('actions.json', 'actions_old.json')
                        with open('actions.json', 'wb') as f:
                            for chunk in r.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)
                    break


def question(api, update):
    settings = getSettings()
    api.messages.send(peer_id=update[3],
                      message=random.choice(settings['messages']['possible']).format(str(random.randint(0, 100))))

def schedule_new(api, update):
    group = '17'

    if len(str(update[6]).lower().split(' ')) > 1:
        group = str(update[6]).lower().split(' ')[1]
    api.messages.send(peer_id=update[3], message=msce.parseGroup(group,
                                                    random.choice(getSettings()['messages']['schedule_not_exist'])))

def isAdmin(update):
    settings = getSettings()
    for admin in settings['admin_ids']:
        if admin in str(update[3]):
            return True
    return False

def actionManager(api, update, action):
    settings = getSettings()
    if action == 'schedule_new':
        schedule_new(api, update)
    elif action == 'settings_get':
        sender.sendDoc(api, update[3], 'actions.json')
    elif action == 'random':
        question(api, update)
    elif action == 'settings_send':
        if isAdmin(update):
            saveDoc(api, update)
        else:
            api.messages.send(peer_id=update[3], message=random.choice(settings['messages']['not_admin']))
    else:
        if action in settings['messages']:
            api.messages.send(peer_id=update[3], message=random.choice(settings['messages'][action]))



def message(api, update):
    settings = getSettings()
    settings = settings['new_message']
    if 'attach1_type' in update[-1]:
        if update[-1]['attach1_type'] == 'sticker':
            for setting in settings:
                if 'stickers' in setting:
                    for sticker in setting['stickers']:
                        if sticker == '{}_{}'.format(update[-1]['attach1_product_id'], update[-1]['attach1']):
                            actionManager(api, update, setting['action'])
                            break
    for setting in settings:
        for quote in setting['quotes']:
            if str(update[6]).lower().startswith(quote):
                actionManager(api, update, setting['action'])
                break


if saver.openPref('me', 'login', None) is None:
    login = input('Number or email: ')
    password = input('Password: ')
else:
    login = saver.openPref('me', 'login', None)
    password = saver.openPref('me', 'password', None)

try:
    api = vk_requests.create_api(app_id=app_id, login=login,
                                 password=password, scope=permissions, api_version='5.62')
    if saver.openPref('me', 'login', None) is None:
        saver.savePref('me', 'login', login)
        saver.savePref('me', 'password', password)
except Exception as ex:
    print(ex.__str__())
VKPooler.addHandler(Codes.NEW_MESSAGE, message)
VKPooler.startPooling(api)
