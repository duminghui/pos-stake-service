#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import time
from time import struct_time


class Dict(dict):
    '''
    Simple dict but support access as x.y style.
    '''

    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


def toDict(d):
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D


def get_gmt_time_yyyymmddhhmmss(timestamp=time.gmtime(time.time())):
    if not isinstance(timestamp, struct_time):
        timestamp = time.gmtime(timestamp)
    str_time = time.strftime('%Y-%m-%d %H:%M:%S', timestamp)
    return str_time


def get_gmt_time_yyyymmdd(timestamp=time.gmtime(time.time())):
    if not isinstance(timestamp, struct_time):
        timestamp = time.gmtime(timestamp)
    str_time = time.strftime('%Y-%m-%d', timestamp)
    return str_time


def get_timestamp_daily_last_second(timestamp):
    time_str = '%s 23:59:59' % (get_gmt_time_yyyymmdd(timestamp))
    return int(time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S')))


if __name__ == '__main__':
    print(get_gmt_time_yyyymmddhhmmss(1524009599 + 1))
    print(get_timestamp_daily_last_second(time.time()))
    i = 10
    # i += 1
    i += (4 + 3)
    print(i)
# print(get_gmt_time_yyyymmdd(time.time()))
# print(get_gmt_time_yyyymmddhhmmss(1))
