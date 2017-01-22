import requests

def parseSubGroups(lesson, audience):
    import re
    lesson.strip()
    numbers = re.sub("[^-?0-9]+", ' ', lesson)
    search = numbers.strip().split(' ')
    rooms = audience.strip().split(' ')

    if len(rooms) == len(search):
        result = ""
        i = 1
        while i < len(search):
            result += lesson.split(search[i])[0] + " || кабинет: " + \
                      rooms[i - 1] + "\n"
            lesson = lesson[lesson.index(search[i]):]
            i += 1
        result += lesson + " || кабинет: " + \
                  rooms[len(rooms) - 1] + "\n"
        return result
    else:
        return lesson + " || кабинет(кабинеты): " + rooms

def parseGroup(group):
    s = '                                                  \n'
    # API
    r = requests.get('http://s1.al3xable.me/method/getStudent?group={}'.format(group))
    if r.json()['code'] == 0:
        lessons = r.json()
        for index, d in enumerate(lessons['data']['groups']):
            for k in lessons['data']['groups'][index]['lessons']:
                s = s + 'Номер пары: ' + str(k['number']) + '\n'
                s += parseSubGroups(k['lesson'], k['audience'])
                s = s + '                                                  \n'
        return s
    else:
        return 'Либо такой группы нет, либо сервер упал, либо Тоха питух'
