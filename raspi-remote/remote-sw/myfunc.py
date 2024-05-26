#!/usr/bin/python3

from flask import Flask,request,Response
import json
from raspi import init_gpio, power_sw, power_on, power_off

def version():
    return 'version 0.1'


def get_param(param):
    print(param)
    val = request.args.get(param)
    print(val)
    return 'param, {}!'.format(val)

def post_param(param):
    val = request.form.get(param)
    return param + ' = ' + val


def command():
    json_data = request.get_json()
    if not json_data:
        return {"message": "Must provide message to send to slack"}, 400

    try:
        message  = json_data['message']
        password = json_data['password']
    except KeyError as err:
        return {"message": "Must provide message to send to slack"}, 422

    print(message)
    print(password)
    
    rst = json.dumps(json_data)
    resp = Response(rst, 200, mimetype='application/json')

    return resp
    

def raspi():
    json_data = request.get_json()
    if not json_data:
        return {"rslt": "Must provide JSON message"}, 400
    try:
        pin = json_data['pin']
        keep = json_data['keep']        
    except KeyError as err:
        return {"rslt": err}, 422

    rst = json.dumps({'rslt': power_sw(int(pin),int(keep))})
    return Response(rst, 200, mimetype='application/json')


def raspi_on():
    json_data = request.get_json()
    if not json_data:
        return {"rslt": "Must provide JSON message"}, 400
    try:
        pin = json_data['pin']
    except KeyError as err:
        return {"rslt": err}, 422

    rst = json.dumps({'rslt': power_on(int(pin))})
    return Response(rst, 200, mimetype='application/json')


def raspi_off():
    json_data = request.get_json()
    if not json_data:
        return {"rslt": "Must provide JSON message"}, 400
    try:
        pin = json_data['pin']
    except KeyError as err:
        return {"rslt": err}, 422

    rst = json.dumps({'rslt': power_off(int(pin))})
    return Response(rst, 200, mimetype='application/json')
