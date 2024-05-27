#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# 2015/8/9 データロガーフレームワーク
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
    mqttc.publish(pub, json_msg)
    #print json_msg


#
# メインループ
#
def main_loop():

    # センサー計測、ここでデータを文字列化して、MQTTブローカーに送信する

    while True:
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
        rc = mqttc.loop(timeout=5000.0)
        time.sleep(5) 


###
if __name__ == '__main__':
    global mqttc

    load_config()
    mqttc = paho.Client()


    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.connect(mqtt_broker["url"], int(mqtt_broker["port"]))

    # 各種センサー初期化
    tp.init()
    pw.init()
    ap.init()

    # Start subscribe, with QoS level 0
    #mqttc.subscribe("sensor/ctrl", 0)
    main_loop()

###

