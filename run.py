import vk_requests
import logging
import getpass
from vk_polling import VKPooler
from vk_polling.VKPooler import Codes

logging.basicConfig(level=logging.DEBUG)

def Message(api, update):
    print('New message!')
    print(update)

def Online(api, update):
    print('User {} is online'.format(-update[1]))

login = input('Number or email: ')
password = getpass.getpass('Password: ')
app_id = 5037590

api = vk_requests.create_api(app_id=app_id, login=login,
                             password=password, scope=['offline', 'messages', 'documents'])

VKPooler.addHandler(Codes.NEW_MESSAGE, Message)
VKPooler.addHandler(Codes.USER_ONLINE, Online)
VKPooler.startPooling(api)



