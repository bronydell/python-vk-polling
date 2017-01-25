import requests

def sendAudioMessage(api, peer_id,filename):

    resp = api.docs.getUploadServer(type='audio_message')
    r = requests.post(resp['upload_url'], files={'file': open(filename, 'rb')})
    resp = r.json()
    resp = api.docs.save(file=resp['file'])

    api.messages.send(peer_id=peer_id,
                             attachment='doc' + str(resp[0]['owner_id']) + '_' + str(resp[0]['id']))

def sendDoc(api, peer_id,filename):
    resp = api.docs.getUploadServer()
    r = requests.post(resp['upload_url'], files={'file': open(filename, 'rb')})
    resp = r.json()
    resp = api.docs.save(file=resp['file'])

    api.messages.send(peer_id=peer_id,
                             attachment='doc' + str(resp[0]['owner_id']) + '_' + str(resp[0]['id']))