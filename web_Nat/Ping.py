#!/usr/bin/env python
# coding:utf-8
import os


def ping(url):
    result = os.system('ping ' + url)
    # if result:
    #     print('ping fail')
    # else:
    #     print('ping ok')
    return result
