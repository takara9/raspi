# ラズパイをGPIO RESTサーバーにするデーモン


これは Raspberry Pi の REST API で操作するためプログラムです。



## インストール方法

OSは、Raspberry Pi OS です。Ubuntuでは確認していません。


```
git clone
sudo make install
```



## REST-APIコール方法

インストールしたpingできるPCなどから、curlでアクセスできます。



### GPIO 2 ピンを 300ミリ秒 ONにする

```
curl -X POST http://rp1:8000/api/v1/raspi -H 'Content-Type: application/json'  -d '{"pin":"2","keep":"300"}'
```


### GPIO 2 ピンを ON にする

```
curl -X POST http://rp1:8000/api/v1/on -H 'Content-Type: application/json'  -d '{"pin":"2"}'
```



### GPIO 2 ピンを OFF にする

```
curl -X POST http://rp1:8000/api/v1/off -H 'Content-Type: application/json'  -d '{"pin":"2"}'
```






