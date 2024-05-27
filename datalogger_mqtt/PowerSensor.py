#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 2015/8/9 Maho Takara
#

import sys
import os
import time

import RPi.GPIO as GPIO

#
# インタフェースの初期化
#
def init():

   global spi_clk
   global spi_mosi
   global spi_miso
   global spi_ss

   # GPIOの番号の定義。
   spi_clk  = 11
   spi_mosi = 10
   spi_miso = 9
   spi_ss   = 8

   # RPiモジュールの設定
   GPIO.setwarnings(False)
   GPIO.setmode(GPIO.BCM)

   # GPIOデバイスの設定
   GPIO.setup(spi_mosi, GPIO.OUT)
   GPIO.setup(spi_miso, GPIO.IN)
   GPIO.setup(spi_clk,  GPIO.OUT)
   GPIO.setup(spi_ss,   GPIO.OUT)


#
# AD変換からのデータ読取り 
#
def read_ad():
   n_samples = 200
   ch = 0
   bt = time.time()

   a_rt = [0] * n_samples
   a_mv = [0] * n_samples
   a_am = [0] * n_samples
   a_pw = [0] * n_samples

   v_rt = [0] * n_samples
   v_mv = [0] * n_samples
   v_am = [0] * n_samples
   v_pw = [0] * n_samples

   x_rt = [0] * n_samples
   x_mv = [0] * n_samples
   x_am = [0] * n_samples
   x_pw = [0] * n_samples

   # 0.1秒インターバルの永久ループ
   for c in range(n_samples):
      time.sleep(0.01)
      GPIO.output(spi_ss,   False)
      GPIO.output(spi_clk,  False)
      GPIO.output(spi_mosi, False)
      GPIO.output(spi_clk,  True)
      GPIO.output(spi_clk,  False)

      # 測定するチャンネルの指定をADコンバータに送信
      cmd = (ch | 0x18) << 3
      for i in range(5):
         if (cmd & 0x80):
            GPIO.output(spi_mosi, True)
         else:
            GPIO.output(spi_mosi, False)
         cmd <<= 1
         GPIO.output(spi_clk, True)
         GPIO.output(spi_clk, False)
      GPIO.output(spi_clk, True)
      GPIO.output(spi_clk, False)
      GPIO.output(spi_clk, True)
      GPIO.output(spi_clk, False)

      # 12ビットの測定結果をADコンバータから受信
      value = 0
      for i in range(12):
         value <<= 1
         GPIO.output(spi_clk, True)
         if (GPIO.input(spi_miso)):
            value |= 0x1
         GPIO.output(spi_clk, False)
      #            
      GPIO.output(spi_ss, True)

      # 測定結果を標準出力
      a_rt[c] = time.time() - bt
      a_mv[c] = value * 3.3 / 4096 * 1000
      a_am[c] = a_mv[c] * 8.5
      a_pw[c] = a_am[c]/1000 * 100

### フィルター 電圧ありだけ
   i = 0
   pw = 0
   for c in range(n_samples):
      if a_am[c] > 0:
         v_rt[i] = a_rt[c]
         v_mv[i] = a_mv[c]
         v_am[i] = a_am[c]
         v_pw[i] = a_pw[c]
         i = i + 1
         pw = pw + a_pw[c]

   av_pw = pw / i

### フィルター １／３以下のデータは除外
   pw = 0
   j = 0
   for c in range(i):
      if v_pw[c] > (av_pw/3):
         x_rt[j] = v_rt[c]
         x_mv[j] = v_mv[c]
         x_am[j] = v_am[c]
         x_pw[j] = v_pw[c]
         j = j + 1
         pw = pw + v_pw[c]
         
   return (pw / j)

###
def get():
   return (0, {"power" : int(read_ad())})
###
