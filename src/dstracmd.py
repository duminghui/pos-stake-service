#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

from enum import Enum, unique
from subprocess import Popen, PIPE
import json
from json.decoder import JSONDecodeError
import logging
from utils import toDict


def __cmd(cmd):
    cmd_result = ''
    cmdStr = "/root/dstrad %s" % cmd
    # logging.info("cmd:%s" % cmdStr)
    cmd_result_cxt = Popen(cmdStr, stdout=PIPE, shell=True).stdout.read().decode("utf-8")
    try:
        data = json.loads(cmd_result_cxt)
        if isinstance(data, dict):
            cmd_result = toDict(data)
        elif isinstance(data, list):
            dictData = []
            for d in data:
                dictData.append(toDict(d))
            cmd_result = dictData
    except JSONDecodeError:
        raise Exception(cmd_result_cxt)
    return cmd_result


def getinfo():
    return __cmd("getinfo")


def listtransactions(count, frm):
    """
    这个命令获取的数据是按时间正序排列的
    :param count:
    :param frm:
    :return:
    """
    # return __cmd("listtransactions '*' %s %s" % (count, frm))
    return __cmd("listtransactions airdrop %s %s" % (count, frm))


def gettransaction(txid):
    return __cmd("gettransaction %s" % txid)


def getbestblockhash():
    cmd_result = ''
    cmdStr = "/root/dstrad getbestblockhash"
    # logging.info("cmd:%s" % cmdStr)
    cmd_result_cxt = Popen(cmdStr, stdout=PIPE, shell=True).stdout.read().decode("utf-8")
    return cmd_result_cxt


def getbestblock():
    return __cmd("getblock {}".format(getbestblockhash()))
