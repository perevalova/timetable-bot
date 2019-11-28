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
                    return print(answer_string)
            elif sel_time < time_sel_item:
                nx1 = ' - '.join(d[keyword][i])
                nx2 = ' - '.join(d[keyword][i + 1])
                answer_string += f'Наступний: {nx1}\n'
                answer_string += f'Наступний: {nx2}\n'
                return answer_string
            elif time_last_bus < sel_time:
                return 'На сьогодні автобусів більше немає'


def all_buses(keyword):
    json_file_path = 'schedule.json'
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
    if message in  ['now_bs1', 'now_bs2', 'now_zt', 'now_br']:
        sel_time = datetime.now().time()
        sel_list = message[message.find('_'):][1:]
        for i in bus_list2:
            keyword = bus_list2[sel_list]
        answer = find_bus(sel_time, keyword)
        return answer
    # returns list of all buses
    elif message in ['zhytomyr', 'busstation1', 'busstation2', 'berezivka']:
        answer = all_buses(message)
        return answer
    # possibility to set a time
    elif 'житомир' or 'ас1' or 'ас2' or 'березівка' in message:
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


def main():
    but = timetable('busstation2')
    print(but)


if __name__ == '__main__':
    main()