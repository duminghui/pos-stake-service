#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

from multiprocessing import Process

import asyncio
import orm
from config import configs
import logging

import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from apscheduler.schedulers.blocking import BlockingScheduler
from models import *
import dstra_scan_service
from apscheduler.triggers.interval import IntervalTrigger, datetime
import datetime as dt
import dstuserdata


async def init_user():
    await Users(id='404504209241669642', name='dumh').save()
    await Users(id='402631387577974797', name='村长').save()
    await Users(id='401916285929127947', name='Parker Lee').save()
    await Users(id='396837819550662668', name='mako jr').save()
    await Users(id='411932460344016896', name='cat lmao').save()
    await Users(id='407552893806182411', name='lucky168').save()
    await Users(id='403478549379678211', name='baobao').save()
    await Users(id='403341228176965633', name='JWKY').save()


async def init(loop):
    await orm.create_pool(loop=loop, **configs.db)
    scheduler = AsyncIOScheduler()
    scheduler.start()
    await dstra_scan_service.start_scan(scheduler)
    # await dstra_scan_service.__scan_unspents()
    # dailies = await DstDailyProfit.findFields(['sum(all_pos_profit) as all_pos_profit', 'sum(injection) as injection'],
    #                                           'isdailynode=?', [1], groupBy=['profit_time_str', 'profit_time'],
    #                                           orderBy='profit_time desc')
    # for daily in dailies:
    #     print(daily.__getattr__('all_pos_profit'))
    # print(await dstuserdata.all_profit_count())
    # await  init_user()
    # sched.add_job(my_job, 'interval', seconds=5, coalesce=True)
    # tigger = IntervalTrigger(start_date=datetime.now() + dt.timedelta(seconds=5), seconds=20)
    # sched.add_job(my_job2, tigger, coalesce=True)
    # walletBalance = WalletBalance(id=1, balance=100, stake=100)
    # await walletBalance.save()
    # print('------------')


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()
