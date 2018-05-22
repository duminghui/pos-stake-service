#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

from models import *
import orm
import logging
import asyncio
from config import *
import re


async def get_user_deposit(userid):
    deposit = (await DstInOutStake.findFields('sum(`change_amount`) as change_amount',
                                              'userid=? and isonchain=? and change_amount>?',
                                              [userid, 1, 0]))[0].change_amount
    if deposit is None:
        deposit = 0.0
    return deposit


async def get_user_withdraw(userid):
    withdraw = (await DstInOutStake.findFields('sum(`change_amount`) as change_amount',
                                               'userid=? and isonchain=? and change_amount<?',
                                               [userid, 1, 0]))[0].change_amount
    if withdraw is None:
        withdraw = 0.0
    return withdraw


async def get_all_rewards_form_daily():
    pass
    all_rewards = (await DstDailyProfit.findFields('sum(daily_profit) as daily_profit', 'isdailynode=?', [1]))[
        0].daily_profit

    if all_rewards is None:
        all_rewards = 0.0
    return all_rewards


async def get_all_rewards_from_txs():
    pass
    all_rewards = (await DstTransactions.findFields('sum(amount) as amount', 'category=? or category=? or category=?',
                                                    [const.CATEGORY_IMMATURE, const.CATEGORY_GENERATE,
                                                     const.CATEGORY_SENDTOSELF])).amount
    if all_rewards is None:
        all_rewards = 0.0
    return all_rewards


async def get_user_in_out_tx(userid, count=10):
    user_txs = await DstInOutStake.findAll('userid=? and isonchain=?', [userid, 1], orderBy='txtime desc', limit=count)
    return user_txs


async def get_txs(limit=0, page_item_count=30):
    txs = await DstTransactions.findAll(orderBy='txtime desc', limit=(limit, page_item_count))
    return txs


async def get_tx_count():
    tx_count = (await DstTransactions.findFields('count(txid) as txid'))[0].txid
    if tx_count is None:
        tx_count = 0
    return tx_count


async def claim_tx(userid, txid):
    user = await Users.find(userid)
    if not user:
        return -1
    stakeTx = await DstInOutStake.findAll('txid=?', txid)
    if not stakeTx or len(stakeTx) == 0:
        return -2
    if stakeTx[0].userid != const.POS_NOUSER_ID:
        return -3
    stakeTx = stakeTx[0]
    stakeTx.userid = userid
    stakeTx.username = user.name
    stakeTx.isprocess = 0
    stakeTx.stake = 0
    stakeTx.start_amount = 0
    stakeTx.pos_profit = 0
    stakeTx.start_balance = 0
    stakeTx.stage_pos_profit = 0
    await stakeTx.update()
    return 0


async def get_no_owner_amount():
    """获取未认领的额数"""
    _no_owner_amount = await DstInOutStake.findFields('sum(change_amount) as change_amount',
                                                      'userid=? and isonchain=?',
                                                      [const.POS_NOUSER_ID, 1])
    if _no_owner_amount:
        _no_owner_amount = _no_owner_amount[0].change_amount
    else:
        _no_owner_amount = 0

    if _no_owner_amount is None:
        _no_owner_amount = 0
    return _no_owner_amount


async def get_immature_amount():
    _immature_amount = await DstInOutStake.findFields('sum(change_amount) as change_amount',
                                                      'isonchain=? and isprocess=?', [1, 0])
    if _immature_amount:
        _immature_amount = _immature_amount[0].change_amount
    else:
        _immature_amount = 0

    if _immature_amount is None:
        _immature_amount = 0
    return _immature_amount


async def wallet_info():
    _wallet_info = await DstWalletInfo.find(1)
    return _wallet_info


async def get_user_immature_amount(userid):
    _immature_amount = (await DstInOutStake.findFields('sum(change_amount) as change_amount',
                                                       'userid=? and isonchain=? and isprocess=?', [userid, 1, 0]))[
        0].change_amount
    # if _immature_amount:
    #     _immature_amount = _immature_amount[0].change_amount
    # else:
    #     _immature_amount = 0.0

    if _immature_amount is None:
        _immature_amount = 0.0
    return _immature_amount


async def user_first_stake(userid):
    _join_time = await DstInOutStake.findAll('userid=? and isonchain=?', [userid, 1], orderBy='txtime', limit=1)
    if len(_join_time) > 0:
        return _join_time[0]
    else:
        return None


async def user_dailies(userid, limit=0, step=5):
    """
    个人每天收益
    :param userid:
    :param limit:
    :param step:
    :return:
    """
    dailies_profit = await DstDailyProfit.findAll('isdailynode=? and userid=?', [1, userid], orderBy='profit_time desc',
                                                  limit=(limit, step))
    return dailies_profit


async def daily_count(userid):
    _all_profit_count = await DstDailyProfit.findFields('count(dailyflag) as count', 'isdailynode=? and userid=?',
                                                        [1, userid])
    if _all_profit_count:
        return _all_profit_count[0].__getattr__('count')
    else:
        return 0


async def dailies(limit=0, step=5):
    """
    每天收益
    :param limit:
    :param step:
    :return:
    """
    dailies_profit = await DstDailyProfit.findFields(
        ['sum(daily_profit) as daily_profit', 'sum(injection) as injection'],
        'isdailynode=?', [1], groupBy=['profit_time_str', 'profit_time'],
        orderBy='profit_time desc', limit=(limit, step))
    return dailies_profit


async def all_profit(limit=0, step=5):
    _all_profit = await DstDailyProfit.findFields(
        ['sum(all_pos_profit) as all_pos_profit', 'sum(injection) as injection'],
        'isdailynode=?', [1], groupBy=['profit_time_str', 'profit_time'],
        orderBy='profit_time desc', limit=(limit, step))
    return _all_profit


async def all_profit_count():
    _all_profit_count = await DstDailyProfit.findFields('count(dailyflag) as count', 'isdailynode=? and username=?',
                                                        [1, 'dumh'])
    if _all_profit_count:
        return _all_profit_count[0].__getattr__('count')
    else:
        return 0


async def user_stakes(userid, limit=0, step=5):
    stakes = await DstInOutStake.findAll('userid=?', [userid], orderBy='pos_time desc', limit=(limit, step))
    return stakes


async def user_stake_count(userid):
    stake_count = await  DstInOutStake.findNumber('count(userid)', 'userid=?', [userid])
    if stake_count:
        return stake_count
    else:
        return 0


async def init(loop):
    await orm.create_pool(loop=loop, **configs.db)
    stakes = await user_stakes('404504209241669642', 10)
    for user_stake in stakes:
        if user_stake.isonchain:
            change_reason = '新入资金'
        else:
            change_reason = '%s新入资金' % user_stake.change_username
        msg_value = '占比: %s%%\n资金变更: %s\n起始资金: %s\n变更原因: %s\n变更时间: %s'

        str = '占比:    {:>23.15%}\n资金变更:{:>23,.08f}\n起始资金:{:>23,.08f}\n变更时间:{:>23s}\n变更原因:{:>19s}'.format(
            user_stake.stake, user_stake.change_amount, user_stake.start_amount, user_stake.txtime_str, change_reason)
        print(str)
        print('-------------------')


def get_user_id(user_str):
    m = re.match(r'^<@(\d*)>$', '<@404504209241669642>')
    if m:
        return m.group(0)


import dstracmd
import utils


# def m1(a, b, **kw):
#     print('m1', kw)
#     kw['a'] = 'm1a'
#     print(kw)


# def m1(a, b, *, c, **kw):
#     print('a', a, 'b', b, c, kw)

# def turn_page(ctx, func, message=None, *, pageno=1, **kw):
#     print(ctx, func, message, pageno, kw)


# def m1(a, **kw):
#     print('a', a, 'b', ,b, 'c', c, kw)
# print(a, kw)

def turn_page(ctx, func, message=None, pageno=1, **kw):
    print(ctx, func, message, pageno, kw)
    func(ctx, pageno=pageno, **kw)
    pass


def myrewards(ctx, user=None, pageno=1):
    """
    个人每天收益
    :param ctx:
    :param user:
    :param limit:
    :return:
    """

    def create_content(ctx, user=None, pageno=1):
        print(ctx, user, pageno)

    turn_page('ctx', create_content, user='aaa', pageno=100)


if __name__ == '__main__':
    p = {'a': 'aaaa', 'b': 'bbbb'}
    print('{b:},{a:}'.format(**p))
    # myrewards("ctx", None, 100)
    # item_count = 11
    # page_item = 4

    # print(round(9, 14))
    # for item_count in range(1, 14):
    #     max_page = int(item_count / page_item)
    #     print(max_page)
    #     print(item_count > max_page * page_item)
    # max_page += (item_count > max_page * page_item or 0)
    # print(item_count, max_page)
    # print('------')

    # print(int(15 / 5) + 15 % 5)
    # print(int(16 / 5) + (-1 or 1))
    # print(int(17 / 5) + int(5 / 17 % 5))
    # m1(m2, a='a', b='b', pageno=1)
    # logging.getLogger().setLevel(logging.INFO)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(init(loop))
    # loop.run_forever()
    # print('|{:>20.10%}{}'.format(10000000, 10))
    # m = re.match(r'^<@(\d*)>$', '<@404504209241669642>')
    # print(m.group(1))
    # m = re.match(r'^\d*$', '%s' % 0)
    # print(m)
    # _limit = 20
    # user_stake_count = 20
    # print((_limit + 4 if _limit + 4 < user_stake_count else user_stake_count - 1))
    # bestblock = dstracmd.getbestblock()
    # print('bestblock', utils.get_gmt_time_yyyymmddhhmmss(bestblock.time))
    # print('nowtime', utils.get_gmt_time_yyyymmddhhmmss(time.time()))
    # print("fix_time", utils.get_gmt_time_yyyymmddhhmmss(time.time() + dstracmd.getinfo().timeoffset))
    # print('100'.__len__())
    # print('{0.__len__():>15}{:>10}'.format('100', 101))
