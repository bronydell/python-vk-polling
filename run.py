import vk_requests
import logging
import json
import saver
from vk_polling import VKPooler
from vk_polling.VKPooler import Codes
import msce_getter as msce

app_id = 5037590
logging.basicConfig(level=logging.CRITICAL)

def getSettings():
    try:
        with open('actions.json', encoding='UTF-8') as data_file:
            data = json.load(data_file)
            return data
    except Exception as ex:
        print(ex.__str__())

def message(api, update):
    settings = getSettings()
    settings = settings['new_message']
    for setting in settings:
        for quote in setting['quotes']:
            if quote in str(update[6]).lower():
                group = '17'
                if len(str(update[6]).split(' ')) == 2:
                    group = str(update[6]).split(' ')[1]
                api.messages.send(peer_id=update[3], message=msce.parseGroup(group))

def online(api, update):
    user = api.users.get(user_ids=-update[1])[0]
    print('User {} {} is online'.format(user['first_name'], user['last_name']))

if saver.openPref('me', 'login', None) is None:
    login = input('Number or email: ')
    password = input('Password: ')
else:
    login = saver.openPref('me', 'login', None)
    password = saver.openPref('me', 'password', None)

try:
    api = vk_requests.create_api(app_id=app_id, login=login,
                                 password=password, scope=['offline', 'messages', 'documents'])
    if saver.openPref('me', 'login', None) is None:
        saver.savePref('me', 'login', login)
        saver.savePref('me', 'password', password)
except Exception as ex:
    print(ex.__str__())
VKPooler.addHandler(Codes.NEW_MESSAGE, message)
VKPooler.addHandler(Codes.USER_ONLINE, online)
VKPooler.startPooling(api)



