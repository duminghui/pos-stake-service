#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import time
from time import struct_time
import datetime


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


def get_time_days_hhmmss(days, timestamp=None):
    if timestamp is None:
        timestamp = time.gmtime(time.time())
    if not isinstance(timestamp, struct_time):
        timestamp = time.gmtime(timestamp)
    str_time = time.strftime('%H:%M:%S', timestamp)
    str_time = '{} days {}'.format(days, str_time)
    return str_time


def get_gmt_time_yyyymmddhhmmss(timestamp=None):
    if timestamp is None:
        timestamp = time.gmtime(time.time())
    if not isinstance(timestamp, struct_time):
        timestamp = time.gmtime(timestamp)
    str_time = time.strftime('%Y-%m-%d %H:%M:%S', timestamp)
    return str_time


def get_gmt_time_yyyymmdd(timestamp=None):
    if timestamp is None:
        timestamp = time.gmtime(time.time())
    if not isinstance(timestamp, struct_time):
        timestamp = time.gmtime(timestamp)
    str_time = time.strftime('%Y-%m-%d', timestamp)
    return str_time


def get_timestamp_daily_last_second(timestamp):
    time_str = '%s 23:59:59' % (get_gmt_time_yyyymmdd(timestamp))
    return int(time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S')))


run_claim_tx = False


def test():
    global run_claim_tx
    if not run_claim_tx:
        print("######")
        run_claim_tx = True


if __name__ == '__main__':
    # print(get_time_jhhmmss(100 - 1))
    datetime1 = datetime.datetime.utcfromtimestamp(1524537648)
    datetime2 = datetime.datetime.utcfromtimestamp(1524677088)
    datetime3 = datetime2 - datetime1
    print(get_time_days_hhmmss(datetime3.days, datetime3.seconds))

# l1 = [1, 2, 3, 4, 5, 6, 7, 8]
# final_page = False
# l2 = l1[1:] if final_page else l1[1:-1]
# print(l2)
# final_page = True
# l2 = l1[1:] if final_page else l1[1:-1]
# print(l2)
# d1 = toDict({'a': 'a', 'b': 'b', 'c': 'd'})
# print('a' in d1)
# print('d' in d1)
# print(run_claim_tx)
# test()
# print(run_claim_tx)
# test()

# l1 = ['b', 'c', 'd', 'b', 'c', 'a', 'a']
# l2 = sorted(set(l1), key=l1.index)
# print(l1)
# print(l2)
# l1.extend(l2)
# print(l1)
# l2 = ['a', 'b', 'c', 'd']
# print(l2[1:])
# print(l2[0:])
# print(l2[1:-1])
# l2.reverse()
# print(l2)
# d1 = toDict({'a': 'a', 'b': 'b'})
# d1 = {'a': 'a', 'b': 'b'}
# d1['c'] = 'c'
# d1.d = 'd'
# print(d1)
# print(datetime.datetime.utcfromtimestamp(time.time()))
# print(get_gmt_time_yyyymmddhhmmss(1524009599 + 1))
# print(get_timestamp_daily_last_second(time.time()))
# i = 10
# i += 1
# i += (4 + 3)
# print(i)
# print(get_gmt_time_yyyymmdd(time.time()))
# print(get_gmt_time_yyyymmddhhmmss(1))
