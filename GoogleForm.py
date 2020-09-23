# !/usr/bin/python
# -*- coding: utf-8 -*-


# 1FAIpQLSe_NtxJ9lxQ9ewMtZ1hRt8XyrbxamxNZNi5E1MvIsijCnjLTQ

import requests


def Send(id, data=None, **kwargs):
    url = f"https://docs.google.com/forms/u/0/d/e/{id}/formResponse"
    requests.post(url, data or kwargs)


def StoreJoke(name, content, source=True):
    jokeForm = "1FAIpQLSe_NtxJ9lxQ9ewMtZ1hRt8XyrbxamxNZNi5E1MvIsijCnjLTQ"
    Send(jokeForm, {
        "entry.866341572": name,
        "entry.1846785254": content,
        "entry.186773396": "Сенченко" if source else "Другие",
        "fvv": 1
    })
