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

def schedule(message):
    my_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(my_dir, 'schedule.json')
    berezivka = ''
    if 'berezivka' in message:
        with open(json_file_path, 'r') as f:
            d = json.load(f)
            for x in d['Berezivka']:
                pr = ' - '.join(x)
                berezivka += f'{pr}\n'
            return berezivka
    elif 'now_br' in message:
        with open(json_file_path, 'r') as f:
            d = json.load(f)
            cur_time = datetime.now().time()
            for i in range(len(d['Berezivka'])-1):
                k = d['Berezivka'][i]
                l = d['Berezivka'][i+1]
                time_obj = datetime.strptime(k[0],
                                                    '%H:%M').time()
                time_obj2 = datetime.strptime(l[0],
                                                    '%H:%M').time()
                if time_obj < cur_time < time_obj2:
                    pr = ' - '.join(d['Berezivka'][i])
                    nx1 = ' - '.join(d['Berezivka'][i+1])
                    nx2 = ' - '.join(d['Berezivka'][i+2])
                    berezivka += f'Попередній: {pr}\n'
                    berezivka += f'Наступний: {nx1}\n'
                    berezivka += f'Наступний: {nx2}\n'
                    return berezivka
                elif time_obj == cur_time:
                    pr = ' - '.join(d['Berezivka'][i-1])
                    nw = ' - '.join(d['Berezivka'][i])
                    nx1 = ' - '.join(d['Berezivka'][i+1])
                    nx2 = ' - '.join(d['Berezivka'][i+2])
                    berezivka += f'Попередній: {pr}\n'
                    berezivka += f'Зараз: {nw}\n'
                    berezivka += f'Наступний: {nx1}\n'
                    berezivka += f'Наступний: {nx2}\n'
                    return berezivka
                elif cur_time < time_obj:
                    nx1 = ' - '.join(d['Berezivka'][i])
                    nx2 = ' - '.join(d['Berezivka'][i+1])
                    berezivka += f'Наступний: {nx1}\n'
                    berezivka += f'Наступний: {nx2}\n'
                    return berezivka
                # elif time_obj < cur_time:
                #     return 'На сьогодні автобусів більше немає'
    else:
        with open(json_file_path, 'r') as f:
            d = json.load(f)
            cur_time = datetime.strptime(message, '%H:%M').time()
            for i in range(len(d['Berezivka'])-1):
                k = d['Berezivka'][i]
                l = d['Berezivka'][i+1]
                time_obj = datetime.strptime(k[0],
                                                    '%H:%M').time()
                time_obj2 = datetime.strptime(l[0],
                                                    '%H:%M').time()
                if time_obj < cur_time < time_obj2:
                    pr = ' - '.join(d['Berezivka'][i])
                    nx1 = ' - '.join(d['Berezivka'][i+1])
                    nx2 = ' - '.join(d['Berezivka'][i+2])
                    berezivka += f'Попередній: {pr}\n'
                    berezivka += f'Наступний: {nx1}\n'
                    berezivka += f'Наступний: {nx2}\n'
                    return berezivka
                elif time_obj == cur_time:
                    pr = ' - '.join(d['Berezivka'][i-1])
                    nw = ' - '.join(d['Berezivka'][i])
                    nx1 = ' - '.join(d['Berezivka'][i+1])
                    nx2 = ' - '.join(d['Berezivka'][i+2])
                    berezivka += f'Попередній: {pr}\n'
                    berezivka += f'Зараз: {nw}\n'
                    berezivka += f'Наступний: {nx1}\n'
                    berezivka += f'Наступний: {nx2}\n'
                    return berezivka
                elif cur_time < time_obj:
                    nx1 = ' - '.join(d['Berezivka'][i])
                    nx2 = ' - '.join(d['Berezivka'][i+1])
                    berezivka += f'Наступний: {nx1}\n'
                    berezivka += f'Наступний: {nx2}\n'
                    return berezivka
                # elif time_obj < cur_time:
                #     return 'На сьогодні автобусів більше немає'

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
                send_message(chat_id, text='Оберіть команду в меню')
            else:
                bus = schedule(mess)
                send_message(chat_id, text=bus)
        else:
            bus = schedule(message)
            send_message(chat_id, text=bus)
        return jsonify(r)
    return '<h1>Bot welcomes you</h1>'


if __name__ == '__main__':
    app.run()
