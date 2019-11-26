import os

import requests
import json
import re
from datetime import datetime
import time

os.environ["TZ"] = "Europe/Kiev"
time.tzset()

def parse_text(text):
    pattern = r'/\w+'
    com = re.search(pattern, text).group()
    # print(com)
    return com[1:]

def find_bus(sel_time, keyword):
    json_file_path = 'schedule.json'
    answer_string = ''
    with open(json_file_path, 'r') as f:
        d = json.load(f)
        for i in range(len(d[keyword]) - 1):
            k = d[keyword][i]
            l = d[keyword][i + 1]
            time_obj = datetime.strptime(k[0],
                                         '%H:%M').time()
            time_obj2 = datetime.strptime(l[0],
                                          '%H:%M').time()
            if time_obj < sel_time < time_obj2:
                pr = ' - '.join(d[keyword][i])
                nx1 = ' - '.join(d[keyword][i + 1])
                answer_string += f'Попередній: {pr}\n'
                answer_string += f'Наступний: {nx1}\n'
                try:
                    nx2 = ' - '.join(d[keyword][i + 2])
                    answer_string += f'Наступний: {nx2}\n'
                    return print(answer_string)
                except IndexError:
                    return print(answer_string)
            elif time_obj == sel_time:
                pr = ' - '.join(d[keyword][i - 1])
                nw = ' - '.join(d[keyword][i])
                answer_string += f'Попередній: {pr}\n'
                answer_string += f'Зараз: {nw}\n'
                try:
                    nx1 = ' - '.join(d[keyword][i + 1])
                    answer_string += f'Наступний: {nx1}\n'
                    nx2 = ' - '.join(d[keyword][i + 2])
                    answer_string += f'Наступний: {nx2}\n'
                    return print(answer_string)
                except IndexError:
                    return print(answer_string)
            elif sel_time < time_obj:
                nx1 = ' - '.join(d[keyword][i])
                nx2 = ' - '.join(d[keyword][i + 1])
                answer_string += f'Наступний: {nx1}\n'
                answer_string += f'Наступний: {nx2}\n'
                return print(answer_string)
            elif datetime.strptime('20:15', '%H:%M').time() < sel_time:
                return print('На сьогодні автобусів більше немає')


def all_buses(keyword):
    json_file_path = 'schedule.json'
    answer_string = ''
    with open(json_file_path, 'r') as f:
        d = json.load(f)
        for x in d[keyword]:
            pr = ' - '.join(x)
            answer_string += f'{pr}\n'
        return print(answer_string)

def timetable(message):
    options = ['zhytomyr', 'busstasion1', 'busstasion2', 'berezivka']
    bus_list = {
        ('bs1', 'ас1'): 'busstation1',
        ('bs2', 'ас2'): 'busstation2',
        ('zt', 'житомир'): 'zhytomyr',
        ('br', 'березівка'): 'berezivka',
    }
    bus_list1 = {
        'ас1': 'busstation1',
        'ас2': 'busstation2',
        'житомир': 'zhytomyr',
        'березівка': 'berezivka',
    }
    bus_list2 = {
        'bs1': 'busstation1',
        'bs2': 'busstation2',
        'zt': 'zhytomyr',
        'br': 'berezivka',
    }
    # for current time
    if 'now_bs1' or 'now_bs2' or 'now_zt'  or 'now_br' in message:
        sel_time = datetime.now().time()
        sel_list = message[message.find('_'):][1:]
        for i in bus_list2:
            keyword = bus_list2[sel_list]
        find_bus(sel_time, keyword)
    # returns list of all buses
    elif 'zhytomyr' or 'busstasion1' or 'busstasion2' or 'berezivka' in message:
        all_buses(message)
    # possibility to set a time
    elif 'житомир' or 'ас1' or 'ас2' or 'березівка' in message:
        try:
            first, last = message.split()
            sel_time = datetime.strptime(last, '%H:%M').time()
            for i in bus_list1:
                keyword = bus_list1[first]
            find_bus(sel_time, keyword)
        except:
            print('Error')


def schedule(message):
    # my_dir = os.path.dirname(__file__)
    # json_file_path = os.path.join(my_dir, 'schedule.json')
    json_file_path = 'schedule.json'
    answer_string = ''
    with open(json_file_path, 'r') as f:
        d = json.load(f)
    # Buses that leave now from Zhytomyr BS1
    if 'now_bs1' in message:
        cur_time = datetime.now().time()
        for i in range(len(d['BS1']) - 1):
            k = d['BS1'][i]
            l = d['BS1'][i + 1]
            time_obj = datetime.strptime(k[0],
                                         '%H:%M').time()
            time_obj2 = datetime.strptime(l[0],
                                          '%H:%M').time()
            if time_obj < cur_time < time_obj2:
                pr = ' - '.join(d['BS1'][i])
                nx1 = ' - '.join(d['BS1'][i + 1])
                answer_string += f'Попередній: {pr}\n'
                answer_string += f'Наступний: {nx1}\n'
                try:
                    nx2 = ' - '.join(d['BS1'][i + 2])
                    answer_string += f'Наступний: {nx2}\n'
                    return print(answer_string)
                except IndexError:
                    return print(answer_string)
            elif time_obj == cur_time:
                pr = ' - '.join(d['BS1'][i - 1])
                nw = ' - '.join(d['BS1'][i])
                answer_string += f'Попередній: {pr}\n'
                answer_string += f'Зараз: {nw}\n'
                try:
                    nx1 = ' - '.join(d['BS1'][i + 1])
                    answer_string += f'Наступний: {nx1}\n'
                    nx2 = ' - '.join(d['BS1'][i + 2])
                    answer_string += f'Наступний: {nx2}\n'
                    return print(answer_string)
                except IndexError:
                    return print(answer_string)
            elif cur_time < time_obj:
                nx1 = ' - '.join(d['BS1'][i])
                nx2 = ' - '.join(d['BS1'][i + 1])
                answer_string += f'Наступний: {nx1}\n'
                answer_string += f'Наступний: {nx2}\n'
                return print(answer_string)
            elif datetime.strptime('20:15', '%H:%M').time() < cur_time:
                return print('На сьогодні автобусів більше немає')
    # Buses that leave now from Berezivka
    elif 'now_br' in message:
        # Berezivka = ''
        cur_time = datetime.now().time()
        for i in range(len(d['Berezivka']) - 1):
            k = d['Berezivka'][i]
            l = d['Berezivka'][i + 1]
            time_obj = datetime.strptime(k[0],
                                         '%H:%M').time()
            time_obj2 = datetime.strptime(l[0],
                                          '%H:%M').time()
            if time_obj < cur_time < time_obj2:
                pr = ' - '.join(d['Berezivka'][i])
                nx1 = ' - '.join(d['Berezivka'][i + 1])
                if d['Berezivka'][i + 2]:
                    nx2 = ' - '.join(d['Berezivka'][i + 2])
                    answer_string += f'Наступний: {nx2}\n'
                answer_string += f'Попередній: {pr}\n'
                answer_string += f'Наступний: {nx1}\n'
                return print(answer_string)
            elif time_obj == cur_time:
                pr = ' - '.join(d['Berezivka'][i - 1])
                nw = ' - '.join(d['Berezivka'][i])
                if d['Berezivka'][i + 1]:
                    nx1 = ' - '.join(d['Berezivka'][i + 1])
                    answer_string += f'Наступний: {nx1}\n'
                if d['Berezivka'][i + 2]:
                    nx2 = ' - '.join(d['Berezivka'][i + 2])
                    answer_string += f'Наступний: {nx2}\n'
                answer_string += f'Попередній: {pr}\n'
                answer_string += f'Зараз: {nw}\n'
                return print(answer_string)
            elif cur_time < time_obj:
                nx1 = ' - '.join(d['Berezivka'][i])
                nx2 = ' - '.join(d['Berezivka'][i + 1])
                answer_string += f'Наступний: {nx1}\n'
                answer_string += f'Наступний: {nx2}\n'
                return print(answer_string)
            elif datetime.strptime('20:15', '%H:%M').time() < cur_time:
                return print('На сьогодні автобусів більше немає')
    # Buses that leave now from Zhytomyr BS2
    elif 'now' in message:
        for x in d['BS1']:
            pr = ' - '.join(x)
            answer_string += f'{pr}\n'
        return print(answer_string)
    # List of all buses from Zhytomyr BS1
    elif 'busstation1' in message:
        for x in d['BS1']:
            pr = ' - '.join(x)
            answer_string += f'{pr}\n'
        return print(answer_string)
    # List of all buses from Zhytomyr BS2
    elif 'busstation2' in message:
        for x in d['BS1']:
            pr = ' - '.join(x)
            answer_string += f'{pr}\n'
        return print(answer_string)
    # List of all buses from Zhytomyr
    elif 'zhytomyr' in message:
        for x in d['BS1']:
            pr = ' - '.join(x)
            answer_string += f'{pr}\n'
        return print(answer_string)
    # List of all buses from Berezivka
    elif 'berezivka' in message:
        for x in d['Berezivka']:
            pr = ' - '.join(x)
            answer_string += f'{pr}\n'
        return print(answer_string)
    else:
        sel_time = datetime.strptime(message, '%H:%M').time()
        for i in range(len(d['Berezivka']) - 1):
            k = d['Berezivka'][i]
            l = d['Berezivka'][i + 1]
            time_obj = datetime.strptime(k[0],
                                         '%H:%M').time()
            time_obj2 = datetime.strptime(l[0],
                                          '%H:%M').time()
            print(time_obj == sel_time)
            if time_obj < sel_time < time_obj2:
                try:
                    pr = ' - '.join(d['Berezivka'][i])
                    nx1 = ' - '.join(d['Berezivka'][i + 1])
                    answer_string += f'Попередній: {pr}\n'
                    answer_string += f'Наступний: {nx1}\n'
                    nx2 = ' - '.join(d['Berezivka'][i + 2])
                    answer_string += f'Наступний: {nx2}\n'
                    return print(answer_string)
                except IndexError:
                    return print(answer_string)
                    # continue
            elif time_obj == sel_time:
                try:
                    print(sel_time)
                    pr = ' - '.join(d['Berezivka'][i - 1])
                    nw = ' - '.join(d['Berezivka'][i])
                    answer_string += f'Попередній: {pr}\n'
                    answer_string += f'Зараз: {nw}\n'
                    nx1 = ' - '.join(d['Berezivka'][i + 1])
                    answer_string += f'Наступний: {nx1}\n'
                    nx2 = ' - '.join(d['Berezivka'][i + 2])
                    answer_string += f'Наступний: {nx2}\n'
                    return print(answer_string)
                except IndexError:
                    return print(answer_string)
            elif sel_time < time_obj:
                nx1 = ' - '.join(d['Berezivka'][i])
                nx2 = ' - '.join(d['Berezivka'][i + 1])
                answer_string += f'Наступний: {nx1}\n'
                answer_string += f'Наступний: {nx2}\n'
                return print(answer_string)
            elif datetime.strptime('20:15', '%H:%M').time() < sel_time:
                return print('На сьогодні автобусів більше немає')


def main():
    all_buses('berezivka')
    timetable('berezivka')


if __name__ == '__main__':
    main()