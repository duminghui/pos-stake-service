#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import time


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


def get_gmt_time_str(timestamp=time.gmtime(time.time())):
    if isinstance(timestamp, int):
        timestamp = time.gmtime(timestamp)
    str_time = time.strftime("%Y-%m-%d %H:%M:%S", timestamp)
    return str_time


if __name__ == '__main__':
    print(get_gmt_time_str(1))
