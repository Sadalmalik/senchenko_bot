# !/usr/bin/python
# -*- coding: utf-8 -*-

import json


data = None


def Load():
    global data
    with open('config.json', 'r', encoding='utf8') as file:
        data = json.load(file)


def Save():
    global data
    with open('config.json', 'w', encoding='utf8') as file:
        js_str = json.dumps(data, indent=2)
        file.write(js_str)
