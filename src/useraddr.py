#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

from models import DstUserAddr

user_addr_map = {}


async def init_user_addr_map():
    global user_addr_map
    userAddrs = await DstUserAddr.findAll()
    for userAddr in userAddrs:
        user_addr_map[userAddr.addr] = userAddr


def get(addr):
    global user_addr_map
    return user_addr_map.get(addr, None)
