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
from .config import token

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

def timetable(message):
    my_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(my_dir, 'schedule.json')
    answer_string = ''
    if 'bs1' in message:
        with open(json_file_path, 'r') as f:
            d = json.load(f)
            for x in d['BS1']:
                pr = ' - '.join(x)
                answer_string += f'{pr}\n'
            return answer_string
    elif 'berezivka' in message:
        with open(json_file_path, 'r') as f:
            d = json.load(f)
            for x in d['answer_string']:
                pr = ' - '.join(x)
                answer_string += f'{pr}\n'
            return answer_string
    elif 'now_br' in message:
        with open(json_file_path, 'r') as f:
            d = json.load(f)
            cur_time = datetime.now().time()
            for i in range(len(d['answer_string'])-1):
                k = d['answer_string'][i]
                l = d['answer_string'][i+1]
                time_obj = datetime.strptime(k[0],
                                                    '%H:%M').time()
                time_obj2 = datetime.strptime(l[0],
                                                    '%H:%M').time()
                if time_obj < cur_time < time_obj2:
                    pr = ' - '.join(d['answer_string'][i])
                    nx1 = ' - '.join(d['answer_string'][i+1])
                    nx2 = ' - '.join(d['answer_string'][i+2])
                    answer_string += f'Попередній: {pr}\n'
                    answer_string += f'Наступний: {nx1}\n'
                    answer_string += f'Наступний: {nx2}\n'
                    return answer_string
                elif time_obj == cur_time:
                    pr = ' - '.join(d['answer_string'][i-1])
                    nw = ' - '.join(d['answer_string'][i])
                    nx1 = ' - '.join(d['answer_string'][i+1])
                    nx2 = ' - '.join(d['answer_string'][i+2])
                    answer_string += f'Попередній: {pr}\n'
                    answer_string += f'Зараз: {nw}\n'
                    answer_string += f'Наступний: {nx1}\n'
                    answer_string += f'Наступний: {nx2}\n'
                    return answer_string
                elif cur_time < time_obj:
                    nx1 = ' - '.join(d['answer_string'][i])
                    nx2 = ' - '.join(d['answer_string'][i+1])
                    answer_string += f'Наступний: {nx1}\n'
                    answer_string += f'Наступний: {nx2}\n'
                    return answer_string
    else:
        with open(json_file_path, 'r') as f:
            d = json.load(f)
            cur_time = datetime.strptime(message, '%H:%M').time()
            for i in range(len(d['answer_string'])-1):
                k = d['answer_string'][i]
                l = d['answer_string'][i+1]
                time_obj = datetime.strptime(k[0],
                                                    '%H:%M').time()
                time_obj2 = datetime.strptime(l[0],
                                                    '%H:%M').time()
                if time_obj < cur_time < time_obj2:
                    pr = ' - '.join(d['answer_string'][i])
                    nx1 = ' - '.join(d['answer_string'][i+1])
                    nx2 = ' - '.join(d['answer_string'][i+2])
                    answer_string += f'Попередній: {pr}\n'
                    answer_string += f'Наступний: {nx1}\n'
                    answer_string += f'Наступний: {nx2}\n'
                    return answer_string
                elif time_obj == cur_time:
                    pr = ' - '.join(d['answer_string'][i-1])
                    nw = ' - '.join(d['answer_string'][i])
                    nx1 = ' - '.join(d['answer_string'][i+1])
                    nx2 = ' - '.join(d['answer_string'][i+2])
                    answer_string += f'Попередній: {pr}\n'
                    answer_string += f'Зараз: {nw}\n'
                    answer_string += f'Наступний: {nx1}\n'
                    answer_string += f'Наступний: {nx2}\n'
                    return answer_string
                elif cur_time < time_obj:
                    nx1 = ' - '.join(d['answer_string'][i])
                    nx2 = ' - '.join(d['answer_string'][i+1])
                    answer_string += f'Наступний: {nx1}\n'
                    answer_string += f'Наступний: {nx2}\n'
                    return answer_string

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
                        '/now - Відправляються в найближчий час з Житомира АС2 \n' \
                        '/now_bs1 - Відправляються в найближчий час з Житомира АС1 \n' \
                        '/now_zt - Відправляються в найближчий час з Житомира \n' \
                        '/now_br - Відправляються в найближчий час з Березівки \n' \
                        '/zhytomyr - Усі автобуси з Житомира \n' \
                        '/busstasion1 - Усі автобуси з Житомира АС1 \n' \
                        '/busstasion2 - Усі автобуси з Житомира АС2 \n' \
                        '/berezivka - Усі автобуси з Березівки \n' \
                        'Також Ви можете ввести пункт відправлення та бажаний час ' \
                        ' у форматі "години:хвилини" для того, щоб запланувати поїздку: \n' \
                        'житомир 14:00 - Запланована поїздка з Житомира \n' \
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
