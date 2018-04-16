#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Models for user, blog, comment.
'''

import time, uuid
import utils
import const

from orm import Model, IntegerField, StringField, BooleanField, FloatField, TextField


def next_id():
    return '%010d%s000' % (int(time.time()), uuid.uuid4().hex[0:6])


if __name__ == '__main__':
    print(next_id())


class WalletBalance(Model):
    __table__ = 'walletBalance'
    id = IntegerField(primary_key=True, default=1)
    balance = FloatField()
    stake = FloatField()
    update_at = FloatField(default=time.time)
    update_at_str = StringField(ddl='varchar(50)', default=utils.get_gmt_time_str)


class Transactions(Model):
    __table__ = 'transactions'
    txid = StringField(primary_key=True, ddl='varchar(50)')
    idx = IntegerField()
    category = StringField(ddl='varchar(20)')
    amount = FloatField()
    txtime = IntegerField()
    txtime_str = StringField(ddl='varchar(50)')


class Users(Model):
    __table__ = 'users'
    id = StringField(primary_key=True, ddl='varchar(50)')
    name = StringField(ddl='varchar(50)')
    create_at = FloatField(default=time.time)
    create_at_time = StringField(ddl='varchar(50)', default=utils.get_gmt_time_str)


class DstInOutStake(Model):
    __table__ = 'dst_in_out_stake'
    id = StringField(ddl='varchar(50)', primary_key=True, default=next_id)
    txid = StringField(ddl='varchar(80)')
    userid = StringField(ddl='varchar(50)', default=const.POS_NOUSER_ID)
    username = StringField(ddl='varchar(50)', default='noname')
    change_amount = FloatField()
    stake = FloatField()
    start_amount = FloatField()
    pos_profit = FloatField()
    fix_amount = FloatField()
    fix_stake = FloatField()
    start_balance = FloatField()
    stage_pos_profit = FloatField()
    txtime = IntegerField()
    txtime_str = StringField(ddl='varchar(50)')
    pos_time = IntegerField()
    pos_time_str = StringField(ddl='varchar(50)')
    isprocess = BooleanField()
    isonchain = BooleanField()
    comment = StringField(ddl='varchar(200)')
