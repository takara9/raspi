#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# 2015/8/9 データロガーフレームワーク
# 2016/1/2 フレームワークの改善
#
# PAHO MQTTのAPIのドキュメントは以下のURL
#  https://www.eclipse.org/paho/clients/python/docs/
# 
#

import sys
import os
import time
import datetime
import locale
import json

# MQTT関連
import paho.mqtt.client as paho
import urlparse

# センサーのドライバーモジュール
import TempSensor as tp
import PowerSensor as pw
import AtmosphericPressureSensor as ap

# GPIO
import RPi.GPIO as GPIO

mqtt_broker = {"url": None, "port": None}
config_file = 'config.json'


def load_config():
    global mqtt_broker
    global config_file

    if mqtt_broker["url"] is None:
        if os.path.isfile(config_file) is False:
            print "The MQTT-Broker infomation is not defined !"
            mqtt_broker["url"] = raw_input("MQTT-Broker url ? (ex; 12.12.12.12 ")
            mqtt_broker["port"] = raw_input("port number ? ")
            with open(config_file, 'w') as f:
                json.dump(mqtt_broker, f, sort_keys=True,indent=4)
        else:
            with open(config_file, 'r') as f:
                mqtt_broker = json.load(f)


###
# Define event callbacks
def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)


#
# 文字列の時間に変換
#
def StringTime(tt):
    ts = time.localtime(tt)
    fmt = "%04d/%02d/%02d,%02d:%02d:%02d"
    return(fmt % (ts.tm_year,ts.tm_mon,ts.tm_mday,ts.tm_hour,ts.tm_min,ts.tm_sec))
    

#
# MQTTブローカーに送信
#
def logger(pub,data):

    # 時刻を追加
    tt = time.time()
    msg = {'uxtm' : int(tt), "sttm" : StringTime(tt) }
    # データをメッセージに追加する
    msg.update(data)

    # JSON形式でMQTTサーバーへ送信
    json_msg = json.dumps(msg)
    rc = mqttc.publish(pub, json_msg)
    #print rc


#
# メインループ
#
def main_loop():

    # MQTTサーバーに接続する
    global mqttc
    mqttc = paho.Client()
    rc = mqttc.connect(mqtt_broker["url"], int(mqtt_broker["port"]))
    #print rc
    #if rc == 0:
    #    GPIO.output(pin, True)
    #else:
    #    GPIO.output(pin, False)

    # センサー計測、ここでデータを文字列化して、MQTTブローカーに送信する
    while True:
        try:
            rc = mqttc.reconnect()
            # MQTTサーバーとのリンクが切れたらエラーLEDを点灯する
            if rc == 0:
                GPIO.output(pin, False)
            else:
                GPIO.output(pin, True)


            # デスクトップの温度
            (rc,data) = tp.get(11,4,"desktop")
            logger("sensor/temp",data)

            # 床上温度
            (rc,data) = tp.get(11,17,"floor")
            logger("sensor/temp",data)

            # 東向き窓のサッシ部分の温度
            (rc,data) = tp.get(11,22,"window")
            logger("sensor/temp",data)

            # 電力消費量 ワット
            (rc,data) = pw.get()
            logger("sensor/power", data)

            # 大気圧 ヘクトパスカル
            (rc,data) = ap.get()
            logger("sensor/pressure", data)

            # 送信応答が返ってくるので、コールバックとして受けておく
            # ループのタイムアウトが良かったがダメだったので、これで一旦対応を保留
            rc = mqttc.loop(timeout=1000.0)
            mqttc.disconnect()
            time.sleep(60) 

        except:
            GPIO.output(pin, True)
            print "Unexpected error:", sys.exc_info()[0]
            time.sleep(5) 


###
if __name__ == '__main__':
    global pin

    # 設定の読み込み
    load_config()

    # エラーLED (GPIO)の初期化
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False) 
    pin = 24
    GPIO.setup(pin, GPIO.OUT)

    # 各センサー初期化
    tp.init()
    pw.init()
    ap.init()

    # Start subscribe, with QoS level 0
    #mqttc.subscribe("sensor/ctrl", 0)
    main_loop()

###

