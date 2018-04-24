#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

import dstuserdata
import logging
import orm
import re
from config import configs
import discord
from discord.ext import commands
import datetime
import asyncio
import const
import time
import pos_bot_config
import utils
from decimal import Decimal

bot = commands.Bot(command_prefix='?')


def get_user_id(user_str):
    m = re.match(r'^<@(\d*)>$', user_str)
    if m:
        return int(m.group(1))


def isnumber(_str):
    m = re.match(r'^\d*$', str(_str))
    if m:
        return True
    else:
        return False


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    await init(bot.loop)
    print('------')


# @bot.event
# async def on_message(message):
#     if message.content.startswith('$thumb'):
#         channel = message.channel
#         bot.add_check()
#         await channel.send('Send me that 👍 reaction, mate')
#         #
#         # def check(reaction, user):
#         #     return user == message.author and str(reaction.emoji) == '👍'
#         #
#         # try:
#         #     reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
#         # except asyncio.TimeoutError:
#         #     await channel.send('👎')
#         # else:
#         #     await channel.send('👍')


@bot.command()
async def test2(ctx):
    embed = discord.Embed(
        title="title ~~(did you know you can have markdown here too?[named links](https://discordapp.com))~~",
        colour=discord.Colour(0x2e3b88), url="https://discordapp.com",
        description="this supports [named links](https://discordapp.com) on top of the previously shown subset of markdown. ```\nyes, even code blocks[named links](https://discordapp.com)```",
        timestamp=datetime.datetime.utcfromtimestamp(time.time()))

    # embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
    # embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    # embed.set_author(name="author name", url="https://discordapp.com",
    #                  icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    # embed.set_footer(text="footer text", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    # embed.set_image(
    #     url='https://cdn.discordapp.com/avatars/404504209241669642/3f5f874ce7c23f82e63a06d64cdc45da.webp?size=1024')
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/404504209241669642/3f5f874ce7c23f82e63a06d64cdc45da.webp?size=1024")
    embed.set_author(name="author name", url="https://discordapp.com",
                     icon_url="https://cdn.discordapp.com/avatars/404504209241669642/3f5f874ce7c23f82e63a06d64cdc45da.webp?size=1024")
    embed.set_footer(text="footer text",
                     icon_url="https://cdn.discordapp.com/avatars/404504209241669642/3f5f874ce7c23f82e63a06d64cdc45da.webp?size=1024")

    embed.add_field(name="🤔", value="some of these properties have certain limits...")
    embed.add_field(name="😱", value="try exceeding some of them!")
    embed.add_field(name="🙄",
                    value="an informative error should show up, and this view will remain as-is until all issues are fixed")
    embed.add_field(name="<:thonkang:219069250692841473> [named links](https://discordapp.com) ",
                    value="these last two [named links](https://discordapp.com) ", inline=False)
    embed.add_field(name="<:thonkang:219069250692841473>",
                    value="are iasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfsadfasdfasdfasdfnline fields", inline=True)
    await ctx.send(
        content="this `supports` __a__ **subset** *of* ~~markdown~~ 😃 ```js\nfunction foo(bar) {\n  console.log(bar);\n}\n\nfoo(1);```",
        embed=embed)


@bot.command()
async def test3(ctx):
    async def createContent(ctx, pageno=1):
        print(ctx.message.author)
        print(pageno)
        return pageno, 'pageno:{}'.format(pageno), None

    await turn_page(ctx, createContent, pageno=1)


@bot.command()
async def test(ctx, a=None, b=None):
    # print(ctx, type(a), type(b), a, b)
    # print(ctx.message.author)
    print(ctx.message)
    print(type(ctx))
    print("####", ctx.message, type(ctx.message))
    if a:
        print(a.split('@'))
    msg = await ctx.send('$name adsfasdfasdf\nadfasdfsadfasdf %s' % a)

    await msg.add_reaction('\N{Black Left-Pointing Triangle}')
    await msg.add_reaction('\N{Black Right-Pointing Triangle}')
    await msg.add_reaction('\N{Down-Pointing Red Triangle}')
    await msg.remove_reaction('\N{Down-Pointing Red Triangle}', ctx.message.author)

    def check(reaction, user):
        msg.remove_reaction(reaction, user)
        # return user == ctx.message.author and str(reaction.emoji) == '\N{THUMBS UP SIGN}'
        return False

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        print('----------------------')
        await msg.edit(content='{0.id}'.format(ctx.message))
        # await msg.remove_reaction('\N{THUMBS UP SIGN}', user)
        await msg.remove_reaction(reaction, user)
    except asyncio.TimeoutError:
        await ctx.send('\N{THUMBS DOWN SIGN}')
        # await msg.clear_reactions()
    else:
        await ctx.send('\N{THUMBS UP SIGN}')
    return False


async def turn_page(ctx, func, message=None, pageno=1, **kw):
    # print('pageno', pageno, 'kw', kw)
    _pageno, msg_content, msg_embed = await func(ctx, pageno=pageno, **kw)
    # print('_pageno', _pageno)
    if message is None:
        message = await ctx.send(msg_content, embed=msg_embed)
        if _pageno != 0:
            await message.add_reaction(const.PAGE_DOWN_EMOJI)
            await message.add_reaction(const.PAGE_UP_EMOJI)
        else:
            return
    else:
        await message.edit(content=msg_content, embed=msg_embed)

    def check(reaction, user):
        return user == ctx.message.author and reaction.message.id == message.id

    try:
        reaction, user = await ctx.bot.wait_for('reaction_add', timeout=15.0, check=check)
    except asyncio.TimeoutError:
        # await message.clear_reactions()
        await message.add_reaction(const.PAGE_LOCK_EMOJI)
        pass
    else:
        if str(reaction.emoji) == const.PAGE_UP_EMOJI:
            pageno = _pageno + 1
        elif str(str(reaction.emoji)) == const.PAGE_DOWN_EMOJI:
            pageno = _pageno - 1
        await message.remove_reaction(reaction, user)
        await turn_page(ctx, func, message, pageno, **kw)


def get_start_end_pageno(pageno, item_count, page_item_count):
    if pageno < 1:
        pageno = 1
    max_pageno = int(item_count / page_item_count)
    max_pageno += (item_count > max_pageno * page_item_count or 0)
    if pageno > max_pageno:
        pageno = max_pageno
    start = (pageno - 1) * page_item_count
    if start < 0:
        start = 0
    end = start + page_item_count
    if end > item_count:
        end = item_count
    return start, end, pageno


def _log(ctx, command, **kw):
    logging.info(
        '[{}][{}],[CMD:{}], args:{}\n'.format(utils.get_gmt_time_yyyymmddhhmmss(), ctx.message.author.name, command,
                                              kw))


@bot.command()
async def profile(ctx, user=None):
    _log(ctx, 'profile', user=user)
    _userid = None
    if user:
        _userid = get_user_id(user)
    if not _userid:
        _userid = ctx.message.author.id
    _user = ctx.bot.get_user(_userid)
    if _user is None:
        await ctx.send('```MD\n Error User```')
        return
    _userid = _user.id
    _username = _user.name
    _daily_profit = await dstuserdata.user_dailies(_userid, 0, 1)
    if len(_daily_profit) == 0:
        stake = 0
        stake_time = utils.get_gmt_time_yyyymmddhhmmss(time.time())
        pos_rewards = 0
        all_pos_rewards = 0
        injection = 0
        immature = 0
        balance = 0
        timestamp = time.time()
        in_out_txs = []
    else:
        stake = _daily_profit[0].stake
        stake_time = utils.get_gmt_time_yyyymmddhhmmss(_daily_profit[0].pos_time)
        pos_rewards = _daily_profit[0].daily_profit
        all_pos_rewards = Decimal(str(_daily_profit[0].all_pos_profit))
        immature = Decimal(str(await dstuserdata.get_user_immature_amount(_userid)))
        injection = (Decimal(str(_daily_profit[0].injection)) + immature).__round__(const.PREC_BALANCE)
        balance = (all_pos_rewards + injection).__round__(const.PREC_BALANCE)
        timestamp = _daily_profit[0].profit_time
        in_out_txs = await dstuserdata.get_user_in_out_tx(_userid)

    embed = discord.Embed(
        # title='{}\' Profile',
        # timestamp=datetime.datetime.utcfromtimestamp(timestamp),
        colour=discord.Colour(0x00FF00))
    dst_template = '{:,} DST'
    # embed.set_thumbnail(url=_user.avatar_url)
    embed.set_author(name='{}\'s Profile'.format(_username), icon_url=_user.avatar_url)
    embed.add_field(name='Today PoS rewards:', value=dst_template.format(pos_rewards), inline=True)
    embed.add_field(name='All PoS rewards:', value=dst_template.format(all_pos_rewards), inline=True)
    embed.add_field(name="Injection:", value=dst_template.format(injection), inline=True)
    embed.add_field(name='Balance:', value=dst_template.format(balance), inline=True)
    embed.add_field(name='Immature:', value=dst_template.format(immature), inline=True)
    embed.add_field(name='Stake:(does not include immature)', value='{:}% ({})'.format(stake * 100, stake_time),
                    inline=False)
    if len(in_out_txs) > 0:
        in_out_tx_template = '({:,} DST) [{}](https://iquidus.dstra.io/tx/{})'
        in_out_tx = ' | '.join(
            map(lambda tx: in_out_tx_template.format(tx.change_amount, tx.txid[:10], tx.txid),
                in_out_txs))
        embed.add_field(name='Last 10 TX:', value=in_out_tx, inline=False)
    embed.set_footer(text='Last Update:{}'.format(utils.get_gmt_time_yyyymmddhhmmss(timestamp)))
    await ctx.send(embed=embed)


@bot.command()
async def txs(ctx, pageno=1):
    _log(ctx, 'txs', pageno=pageno)
    if pageno:
        if not isnumber(pageno):
            pageno = 1
        else:
            pageno = int(pageno)
    else:
        pageno = 1

    async def create_content(ctx, pageno):
        tx_count = await dstuserdata.get_tx_count()
        if tx_count == 0:
            return 0, '```MD\n Don\'t have Transaction```', None
        __limit, __limit_end, __pageno = get_start_end_pageno(pageno, tx_count, 30)
        msg_values = ['```MD', 'Transactions {:}~{}, Total {} items'.format(__limit + 1, __limit_end, tx_count)]
        txs = await dstuserdata.get_txs(__limit)
        for index, tx in enumerate(txs):
            if tx.category == 'immature':
                msg_values.append('{:<5}{:>20}{:>27}'.format('{}.'.format(index + __limit + 1), tx.txtime_str,
                                                             '[{:,} DST]'.format(tx.amount)))
            else:
                # tx_template = '{:<4} {:>13}{:>23,} DST'
                msg_values.append(
                    '{:<5}{:>20}{:>23,} DST'.format('{}.'.format(index + __limit + 1), tx.txtime_str, tx.amount))

        # msg_count = '\n'.join(map(
        #     lambda index_tx: '{:<4} {:>13}{:>23,} DST'.format('{}.'.format(index_tx[0] + __limit + 1),
        #                                                       index_tx[1].txtime_str,
        #                                                       index_tx[1].amount), enumerate(txs)))
        msg_values.append('```')
        return __pageno, '\n'.join(msg_values), None

    await turn_page(ctx, create_content, pageno=pageno)


@bot.command()
async def claimtx(ctx, userid=None, txid=None):
    _log(ctx, 'ctx', userid=userid, txid=txid)
    if not userid or not txid:
        await ctx.send('```MD\nPlease input user and txid```')
        return
    _userid = get_user_id(userid)
    if not _userid:
        await ctx.send('```MD\nPlease input user```')
        return
    result = await dstuserdata.claim_tx(_userid, txid)
    # result = True
    embed = discord.Embed(
        title='Tx claim',
        description='',
        color=0x00FF00)
    if result == 0:
        result_msg = 'SUCCESS, Please wait for 8 hour to start new stake'
    elif result == -1:
        result_msg = 'ERROR, Don\'t had this user in database'
    elif result == -2:
        result_msg = 'ERROR, Don\t had this TX in database, please wait for the scan service to scan this TX, you can use command ?txs to view'
    elif result == -3:
        result_msg = 'ERROR, this TX had owner'
    else:
        result_msg = 'Other ERROR'

    embed.add_field(name='Result:',
                    value='{0} claim Tx [{1}](https://iquidus.dstra.io/tx/{1}) {2}'.format(
                        userid, txid, result_msg))
    await ctx.send(embed=embed)


@bot.command()
async def walletinfo(ctx):
    _log(ctx, 'walletinfo')
    """
    钱包信息
    :param ctx:
    :return:
    """

    embed = discord.Embed(
        title='Wallet Info',
        timestamp=datetime.datetime.utcfromtimestamp(time.time()),
        colour=discord.Colour(0x00FF00))
    embed.set_footer(text='Last Update:')

    _walletinfo = await dstuserdata.wallet_info()
    if _walletinfo:
        no_owner_amount = await dstuserdata.get_no_owner_amount()
        _immature_amount = await  dstuserdata.get_immature_amount()
        dst_template = '{:,} DST'

        embed.timestamp = datetime.datetime.utcfromtimestamp(_walletinfo.update_at)
        embed.add_field(name='Spendable:', value=dst_template.format(_walletinfo.balance), inline=True)
        embed.add_field(name='Stake', value=dst_template.format(_walletinfo.stake), inline=True)
        embed.add_field(name='Total', value=dst_template.format(_walletinfo.balance + _walletinfo.stake), inline=True)
        embed.add_field(name='Immature', value=dst_template.format(_immature_amount), inline=False)
        embed.add_field(name='No Owner', value=dst_template.format(no_owner_amount), inline=False)

        # msg = '```MD\n{:>11}:{:>23,.8f} DST\n{:>11}:{:23,.8f} DST\n{:>11}:{:>23,.8f} DST\n\n{:>11}:{:>23,} DST\n\n{:>11}:{:>27}```'.format(
        #     'Spendable', _walletinfo.balance, 'Stake', _walletinfo.stake, 'Total',
        #     _walletinfo.balance + _walletinfo.stake, "No Owner",
        #     no_owner_amount, "Update Time", _walletinfo.update_at_str
        # )
    else:
        embed.description = '```钱包信息还未更新```'

    await ctx.send(embed=embed)


@bot.command()
async def myrewards(ctx, user=None, pageno=1):
    _log(ctx, 'myrewards', user=user, pageno=pageno)
    """
    个人每天收益
    :param ctx:
    :param user:
    :param pageno:
    :return:
    """
    # print('', user)
    # print("###", ctx.bot.get_user(404504209241669642).id)
    # print("###", ctx.bot.get_user(404504209241669642).name)
    _userid = None
    if user:
        _userid = get_user_id(user)
    if not _userid:
        _userid = ctx.message.author.id

    if user and isnumber(user):
        _pageno = int(user)
    else:
        if isnumber(pageno):
            _pageno = pageno
        else:
            _pageno = 1

    _user = ctx.bot.get_user(_userid)

    # print('#avatar', _user.avatar)
    # print('#avatar_url', _user.avatar_url)
    # print('#default_avatar', _user.default_avatar)
    # print('#default_avatar_url', _user.default_avatar_url)

    async def create_content(ctx, user=None, pageno=1):
        if user is None:
            __userid = -1
            __username = 'Nousername'
        else:
            __userid = user.id
            __username = user.name
        mydailies_count = await dstuserdata.daily_count(_userid)

        if mydailies_count == 0:
            return 0, '```MD\nDon`t have {}` data or pageno error, Total {} items```'.format(__username,
                                                                                             mydailies_count), None
        __limit, __item_end, __pageno = get_start_end_pageno(pageno, mydailies_count, const.PAGE_ITEM_COUNT)

        mydailies = await dstuserdata.user_dailies(__userid, __limit)
        # 'Daily rewards'
        # 'Total rewards'
        # 'Injection'
        # 'Stake'
        msg_single_template = '{}. {}\n{:>15}:{:>19,.8f} DST\n{:>15}:{:>19,.8f} DST\n{:>15}:{:>19,.8f} DST\n{:>15}:{:>23.15%}'
        msg_content = '\n'.join(map(
            lambda x: msg_single_template.format(x[0] + __limit + 1, x[1].profit_time_str, 'Daily rewards',
                                                 x[1].daily_profit, 'Total rewards', x[1].all_pos_profit, 'Injection',
                                                 x[1].injection, 'Stake', x[1].stake), enumerate(mydailies)))
        msg_content = '```MD\n{}\'s daily PoS rewards ({}~{}, total {} items)\n{}```'. \
            format(__username, __limit + 1, __item_end, mydailies_count, msg_content)
        return __pageno, msg_content, None

    await turn_page(ctx, create_content, user=_user, pageno=_pageno)


@bot.command()
async def dailyrewards(ctx, pageno=None):
    _log(ctx, 'dailyrewards', pageno=pageno)

    """
    每天总收益
    :param ctx:
    :param pageno:
    :return:
    """
    if pageno:
        if not isnumber(pageno):
            pageno = 1
        else:
            pageno = int(pageno)
    else:
        pageno = 1

    async def create_content(ctx, pageno):
        dailies_count = await  dstuserdata.all_profit_count()
        if dailies_count == 0:
            return 0, '```MD\n```Total {} times'.format(dailies_count), None

        __limit, __item_end, __pageno = get_start_end_pageno(pageno, dailies_count, const.PAGE_ITEM_COUNT)

        dailies_profit = await dstuserdata.dailies(__limit)

        # 'Daily Total rewards'
        # msg_single_template = '{}.{}\n  Daily total rewards:{:>19,.8f} DST'
        msg_single_template = '{}. {}\n{:>19}:{:>21,.8f} DST\n{:>19}:{:>21,.8f} DST'
        msg = '\n'.join(map(
            lambda x: msg_single_template.format(x[0] + __limit + 1, x[1].profit_time_str, 'Daily total rewards',
                                                 x[1].daily_profit, 'All injection', x[1].injection),
            enumerate(dailies_profit)))

        msg = '```MD\nDaily total PoS rewards ({}~{}, Total {} items)\n{}```'.format(__limit + 1,
                                                                                     __item_end, dailies_count, msg)
        return __pageno, msg, None

    await turn_page(ctx, create_content, pageno=pageno)


@bot.command()
async def allrewards(ctx, pageno=None):
    _log(ctx, 'allrewards', pageno=pageno)
    """
    总收益
    :param ctx:
    :param pageno:
    :return:
    """
    if pageno:
        if not isnumber(pageno):
            pageno = 1
        else:
            pageno = int(pageno)
    else:
        pageno = 1

    async def create_content(ctx, pageno):
        all_profit_count = await dstuserdata.all_profit_count()

        if all_profit_count == 0:
            return 0, '```MD\nTotal {} times```'.format(all_profit_count), None

        __limit, __item_end, __pageno = get_start_end_pageno(pageno, all_profit_count, const.PAGE_ITEM_COUNT)

        all_profit = await dstuserdata.all_profit(__limit)

        # All total rewards
        # All injection
        msg_single_template = '{}. {}\n{:>19}:{:>21,.8f} DST\n{:>19}:{:>21,.8f} DST\n{:>19}:{:>21,.8f} DST'
        msg = '\n'.join(map(
            lambda x: msg_single_template.format(x[0] + __limit + 1, x[1].profit_time_str, 'All total rewards',
                                                 x[1].all_pos_profit, 'All injection', x[1].injection, 'Total',
                                                 x[1].all_pos_profit + x[1].injection),
            enumerate(all_profit)))
        msg = '```MD\nDaily total PoS rewards ({}~{}, total {} items)\n{}```'.format(__limit + 1,
                                                                                     __item_end, all_profit_count,
                                                                                     msg)
        return __pageno, msg, None

    await turn_page(ctx, create_content, pageno=pageno)

    # embed = discord.Embed(
    #     title='总收益:', description='', color=0x00FF00)
    # # for index, daily_profit in enumerate(dailies_profit):
    # msg_value = '\n'.join(
    #     map(lambda x: '{}.{}\n  总收益:{:>23,.08f}\n  总投入:{:>23,.08f}\n'.format(x[0] + limit, x[1].profit_time_str,
    #                                                                          x[1].all_pos_profit,
    #                                                                          x[1].injection),
    #         enumerate(all_profit)))
    #
    # msg_value = '```Python\n{}```'.format(msg_value)
    # name = '({}~{},共{}条)'.format(
    #     limit, (limit + 4 if limit + 4 < all_profit_count else all_profit_count), all_profit_count)
    # embed.add_field(name=name, value=msg_value, inline=False)
    # await ctx.send(embed=embed)


@bot.command()
async def stake(ctx, user=None, pageno=1):
    _log(ctx, 'stake', user=user, pageno=pageno)
    _userid = None
    if user:
        _userid = get_user_id(user)
    if not _userid:
        _userid = ctx.message.author.id

    if user and isnumber(user):
        _pageno = int(user)
    else:
        if isnumber(pageno):
            _pageno = pageno
        else:
            _pageno = 1

    _user = ctx.bot.get_user(_userid)

    async def create_content(ctx, user=None, pageno=1):
        if user is None:
            __userid = -1
            __username = 'Nousername'
        else:
            __userid = user.id
            __username = user.name

        user_stake_count = await dstuserdata.user_stake_count(__userid)
        if user_stake_count == 0:
            return 0, '```MD\nDon`t have {}\'s data or pageno error, Total {} items```'.format(__username,
                                                                                               user_stake_count), None
        __limit, __item_end, __pageno = get_start_end_pageno(pageno, user_stake_count, const.PAGE_ITEM_COUNT)

        msg_values = ['```MD', '({}~{},total {} items)'.format(
            __limit + 1, __item_end, user_stake_count)]

        user_stakes = await dstuserdata.user_stakes(__userid, __limit)
        msg_txs = []
        for index, user_stake in enumerate(user_stakes):
            msg_values.append('{}. PoS start time: {}, Change time: {}'.format(
                index + __limit + 1, user_stake.pos_time_str, user_stake.txtime_str))
            # Stake
            # Change DST
            # Start DST
            # Change Reason
            # TX
            msg_value_singale = ['{:>13}:{:>30.15%}'.format('Stake', user_stake.stake),
                                 '{:>13}:{:>26,.08f} DST'.format('Change DST', user_stake.change_amount),
                                 '{:>13}:{:>26,.08f} DST'.format('Start DST', user_stake.start_amount)]
            if user_stake.isonchain:
                msg_value_singale.append('{:>13}:{:>30}'.format('Change Reason', 'Injection DST'))
                msg_value_singale.append('{:>13}:{:>30}'.format('TX', user_stake.txid[:20]))
                msg_txs.append('[{}](https://iquidus.dstra.io/tx/{})'.format(user_stake.txid[:20], user_stake.txid))
            else:
                change_reason = '{} Injection DST'.format(user_stake.change_username)
                msg_value_singale.append('{:>13}:{:>30}'.format('Change Reason', change_reason))

            msg_values.append('\n'.join(msg_value_singale))
        # '[%s](https://iquidus.dstra.io/tx/%s)' % (user_stake.txid[:20], user_stake.txid)
        msg_values.append('```')
        embed = discord.Embed(
            # title='{}\'s'.format(__username),
            description='\n'.join(msg_values),
            color=0x00FF00)
        embed.set_author(name='{}\'s stake info'.format(__username), icon_url=user.avatar_url)
        # embed.set_thumbnail(url=user.avatar_url)
        if len(msg_txs) > 0:
            embed.add_field(name='Transactions:', value=', '.join(msg_txs), inline=False)
        return __pageno, None, embed

    await turn_page(ctx, create_content, user=_user, pageno=_pageno)


bot.remove_command('help')


@bot.command()
async def help(ctx):
    msg_values = ['PoS bot Commands',
                  '1. ?stake <@user> <pageno>\n User`s stake:\n - ?stake\n - ?stake 1\n - ?stake @xxxx\n - ?stake @xxxx 1`',
                  '2. ?allrewards <pageno>\n All total rewards:\n - ?allrewards\n - ?allrewards 1',
                  '3. ?dailyrewards <pageno>\n Daily total rewards:\n - ?dailyrewards\n - ?dailyrewards 1',
                  '4. ?myrewards <@user> <pageno>\n User\'s daily rewards:\n - ?myrewards\n - ?myrewards 1\n - ?myrewards @xxxx\n - ?myrewards @xxxx 1',
                  '5. ?mywalletinfo\n WalletInfo',
                  '6. ?txs\n All Wallet Transactions',
                  '7. ?profile\n User Profile'
                  ]
    msg_content = '```MD\n{}```'.format('\n'.join(msg_values))
    await ctx.send(msg_content)


async def init(_loop):
    await orm.create_pool(loop=_loop, **configs.db)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    bot.run(pos_bot_config.POS_BOT_TOKEN)
