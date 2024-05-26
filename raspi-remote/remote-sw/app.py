#!/usr/bin/python3
from flask import Flask,request,Response
from myfunc import version, command, get_param, post_param, raspi, raspi_on, raspi_off
from raspi import init_gpio

app = Flask(__name__)

# Version
@app.route("/version", methods=['GET'])
def ver():
    return version()

# パラメータを指定して値を取得
@app.route("/", methods=['GET'])
def get():
    return get_param("message")

@app.route("/", methods=['POST'])
def post():
    return post_param("data")


# JSONのボディを受け取る
@app.route("/json", methods=['POST'])
def post_json():
    return command()


# RASPi操作
@app.route("/api/v1/raspi", methods=['POST'])
def post_raspi():
    return raspi()

@app.route("/api/v1/on", methods=['POST'])
def post_on():
    return raspi_on()

@app.route("/api/v1/off", methods=['POST'])
def post_off():
    return raspi_off()


if __name__ == "__main__":
    # ポートの初期化
    init_gpio(2)
    init_gpio(3)
    init_gpio(17)
    init_gpio(27)
    # Webサーバーの開始
    app.run(debug=False, host='0.0.0.0', port=8000)
