import json
from datetime import datetime
import os
import re

import requests
from flask import Flask
from flask import jsonify
from flask import request

from flask_sslify import SSLify
import time
from bot.config import token

os.environ["TZ"] = "Europe/Kiev"
time.tzset()

app = Flask(__name__)
sslify = SSLify(app)

URL = f'https://api.telegram.org/bot{token}'

def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def send_message(chat_id, text='Hello'):
    url = f'{URL}/sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()

def parse_text(text):
    pattern = r'/\w+'
    com = re.search(pattern, text).group()
    return com[1:]

# contains file with timetable
my_dir = os.path.dirname(__file__)
json_file_path = os.path.join(my_dir, 'schedule.json')

def find_bus(sel_time, keyword):
    """
    Takes 2 arguments
    :param sel_time: selected time (current time or time entered by the user)
    :param keyword: name of list
    :return: string with answer
    """
    answer_string = ''
    with open(json_file_path, 'r') as f:
        d = json.load(f)
        for i in range(len(d[keyword]) - 1):
            sel_item = d[keyword][i]
            next_item = d[keyword][i + 1]
            last_bus = d[keyword][-1]
            time_sel_item = datetime.strptime(sel_item[0],
                                         '%H:%M').time()
            time_next_item = datetime.strptime(next_item[0],
                                          '%H:%M').time()
            time_last_bus = datetime.strptime(last_bus[0],
                                          '%H:%M').time()
            if time_sel_item < sel_time < time_next_item:
                pr = ' - '.join(d[keyword][i])
                nx1 = ' - '.join(d[keyword][i + 1])
                answer_string += f'Попередній: {pr}\n'
                answer_string += f'Наступний: {nx1}\n'
                try:
                    nx2 = ' - '.join(d[keyword][i + 2])
                    answer_string += f'Наступний: {nx2}\n'
                    return answer_string
                except IndexError:
                    return answer_string
            elif time_sel_item == sel_time:
                pr = ' - '.join(d[keyword][i - 1])
                nw = ' - '.join(d[keyword][i])
                answer_string += f'Попередній: {pr}\n'
                answer_string += f'Зараз: {nw}\n'
                try:
                    nx1 = ' - '.join(d[keyword][i + 1])
                    answer_string += f'Наступний: {nx1}\n'
                    nx2 = ' - '.join(d[keyword][i + 2])
                    answer_string += f'Наступний: {nx2}\n'
                    return answer_string
                except IndexError:
                    return answer_string
            elif sel_time < time_sel_item:
                nx1 = ' - '.join(d[keyword][i])
                nx2 = ' - '.join(d[keyword][i + 1])
                answer_string += f'Наступний: {nx1}\n'
                answer_string += f'Наступний: {nx2}\n'
                return answer_string
            elif time_last_bus < sel_time:
                return 'На сьогодні автобусів більше немає'

def all_buses(keyword):
    """
    Take 1 argument
    :param keyword: name of list
    :return: List of all buses
    """
    answer_string = ''
    with open(json_file_path, 'r') as f:
        d = json.load(f)
        for x in d[keyword]:
            pr = ' - '.join(x)
            answer_string += f'{pr}\n'
        return answer_string

def timetable(message):
    bus_list = {
        ('bs1', 'ас1'): 'busstation1',
        ('bs2', 'ас2'): 'busstation2',
        ('br', 'березівка'): 'berezivka',
    }
    bus_list1 = {
        'ас1': 'busstation1',
        'ас2': 'busstation2',
        'березівка': 'berezivka',
    }
    bus_list2 = {
        'bs1': 'busstation1',
        'bs2': 'busstation2',
        'br': 'berezivka',
    }
    # for current time
    if message in  ['now_bs1', 'now_bs2', 'now_br']:
        sel_time = datetime.now().time()
        sel_list = message[message.find('_'):][1:]
        for i in bus_list2:
            keyword = bus_list2[sel_list]
        answer = find_bus(sel_time, keyword)
        return answer
    # returns list of all buses
    elif message in ['busstation1', 'busstation2', 'berezivka']:
        answer = all_buses(message)
        return answer
    # possibility to set a time
    elif 'ас1' or 'ас2' or 'березівка' in message:
        try:
            first, last = message.split()
            sel_time = datetime.strptime(last, '%H:%M').time()
            for i in bus_list1:
                keyword = bus_list1[first]
            answer = find_bus(sel_time, keyword)
            return answer
        except:
            answer = 'Не коректно введене значення'
            return answer


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        pattern = r'/\w+'
        if re.search(pattern, message):
            mess = parse_text(message)
            if mess == 'start':
                text = 'Вітаю! Цей бот призначений для орієнтації в часі пересування \
                громадського транспорту для села Березівка.'
                text2 = 'Доступні команди: \n' \
                        '/now_bs1 - Відправляються в найближчий час з Житомира АС1 \n' \
                        '/now_bs2 - Відправляються в найближчий час з Житомира АС2 \n' \
                        '/now_br - Відправляються в найближчий час з Березівки \n' \
                        '/busstation1 - Усі автобуси з Житомира АС1 \n' \
                        '/busstation2 - Усі автобуси з Житомира АС2 \n' \
                        '/berezivka - Усі автобуси з Березівки \n' \
                        'Також Ви можете ввести пункт відправлення та бажаний час ' \
                        ' у форматі "години:хвилини" для того, щоб запланувати поїздку: \n' \
                        'ас1 14:00 - Запланована поїздка з Житомира АС1 \n' \
                        'ас2 14:00 - Запланована поїздка з Житомира АС2 \n' \
                        'березівка 14:00 - Запланована поїздка з Березівки'
                send_message(chat_id, text=text)
                send_message(chat_id, text=text2)
            else:
                bus = timetable(mess)
                send_message(chat_id, text=bus)
        else:
            bus = timetable(message)
            send_message(chat_id, text=bus)
        return jsonify(r)
    return '<h1>Bot welcomes you</h1>'


if __name__ == '__main__':
    app.run()
