import requests

class LongPoolServer:
    def __init__(self, url, key, ts):
        self.url = url
        self.key = key
        self.ts = ts

    def getPoolURL(self):
        return ('https://{}?act=a_check&key={}&ts={}&wait=25&mode=2&version=1').format(self.url, self.key, self.ts)

    def pool(self):
        session = requests.session()
        answer = session.get(self.getPoolURL(), timeout=27.0)
        if answer.status_code == 200:
            self.ts = answer.json()['ts']
            return answer.json()
        else:
            raise Exception(
                'Error with get request {}. Answers contains code: {}'.format(answer.url, answer.status_code))

def getLongPoolServer(api):
    answ = api.messages.getLongPollServer()
    server = LongPoolServer(answ['server'], answ['key'], answ['ts'])
    return server

