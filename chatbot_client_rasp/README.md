# Watson 連携I/F (ラズベリーパイ部分)

## v2v_chat_client.js の概要

 Julius で音声認識したテキストを名前付きパイプで受けて
 JSON化したメッセージをMQTTブローカーに送る
 SoftLayerの仮想サーバーで、メッセージを受け取り
 Watson Conversation へ送信、応答を受け取り
 Aques Talk で音声合成する


## chat_client.js
 
 キーボード入力で受けたテキストを MQTTブローカーに送り
 以下同様であるが、
 Aques Talk で出力ではなく、画面にテキスト表示





