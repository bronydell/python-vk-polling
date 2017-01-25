from enum import Enum
from vk_polling import Longpoolserver as poll
import logging
import traceback

functions = {}

def addHandler(code, function):
    if code.value in functions:
        functions[code.value].append(function)
    else:
        functions[code.value] = [function]

class Codes(Enum):
    FLAG_CHANGED = 1
    FLAG_SETUPED = 2
    FLAG_RESETED = 3
    FLAG_CHANGED_COMMUNITY = 11
    FLAG_SETUPED_COMMUNITY = 12
    FLAG_RESETED_COMMUNITY = 10
    NEW_MESSAGE = 4
    READ_INCOMING_MESSAGES = 6
    READ_OUTCOMING_MESSAGES = 7
    USER_ONLINE = 8
    USER_GONE_OFFLINE = 9
    CHAT_NAME_CHANGED = 51
    USER_TYPING_PRIVATE = 61
    USER_TYPING_CHAT = 62
    USER_CALLS = 70
    UNREAD_MESSAGES_COUNTER_UPDATE = 80
    NOTIFICATIONS_SETTINGS_UPDATE = 114



class Errors(Enum):
    HISTORY_FAILED = 1
    KEY_IS_NOT_VALID = 2
    USER_INFO_LOST = 3
    VERSION_IS_NOT_VALID = 4


errors = {Errors.HISTORY_FAILED: 'Error with history ot ts event',
          Errors.KEY_IS_NOT_VALID: 'Key is not valid. Relogin pls',
          Errors.USER_INFO_LOST: 'Restart it with new key',
          Errors.VERSION_IS_NOT_VALID: 'Minimal(ot maximal) version is wrong'}

def startPooling(api):
    server = poll.getLongPoolServer(api)
    while True:
        try:
            answ = server.pool()
            if 'error' in answ:
                for error in Errors:
                    if error.value == answ['error']:
                        logging.error(errors[error.value])
                        server = poll.getLongPoolServer(api)
            else:
                for update in answ['updates']:
                    for code in Codes:
                        if update[0] == code.value:
                            if code.value in functions:
                                for function in functions[code.value]:
                                    function(api, update)
        except Exception as ex:
            server = poll.getLongPoolServer(api)
            print(traceback.format_exc())



