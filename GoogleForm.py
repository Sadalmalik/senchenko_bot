# !/usr/bin/python
# -*- coding: utf-8 -*-


# 1FAIpQLSe_NtxJ9lxQ9ewMtZ1hRt8XyrbxamxNZNi5E1MvIsijCnjLTQ

import requests


def Send(id, data=None, **kwargs):
    url = f"https://docs.google.com/forms/u/0/d/e/{id}/formResponse"
    requests.post(url, data or kwargs)
