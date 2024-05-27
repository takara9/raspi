#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#
# 温度と湿度の記録デーモン
#
# 2015/1/2 初版 Maho Takara
# 2015/5/9 修正 dhtreader.read が失敗する様になり、計測が中断することがあるので
#               exceptionの処理を変更 dhtreader.init()を追加
# 2015/8/8 修正 プログラムの構造の全面見直し
#

import sys
import os
import dhtreader

###
def init():
    rc = 0
    if rc == dhtreader.init():
        print("init error")
    return rc

def get(model,pin,pos):
    cnt = 0
    t = 0
    h = 0
    while True:
        try:
            result = dhtreader.read(model,pin)
            if result != None:
                (t,h) = result
                break
            else:
                cnt = cnt + 1
                if cnt > 5:
                    cnt = 99
                    break
                time.sleep(1)
        except:
            print "Unexpected error:", sys.exc_info()[0]

    data = { "pos" : pos, "mdl" : model, "pin" : pin, "tmp" : t, "hmd" : h, "erc" : cnt}
    return (cnt, data)
###

