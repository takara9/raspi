#!/usr/bin/env node
//
// Watson 連携I/F (ラズベリーパイ部分)
// 
// Julius で音声認識したテキストを
// 名前付きパイプで受けて
// MQTTで、SoftLayerの仮想サーバーに送って
// Watson Conversation のリプライを受け取り
// Aques Talk で音声合成する
// 
// Author : Maho Takara  takara@jp.ibm.com
// 2016/11/26  Initial commit
//

var fs = require('fs');
var util = require('util');
const pipe = '/tmp/Julius';

var mqtt    = require('mqtt');
var cnf = require('./etc/client_config.json');
var client  = mqtt.connect(cnf.broker_url);

var param = {encoding: 'utf-8', bufferSize: 1};
var readableStream = fs.createReadStream(pipe, param);
var exec = require('child_process').exec;

// Callback as the connection established
client.on('connect', function () {
    console.log("connect & subscribe");
    client.subscribe(cnf.reply_topic);
});


// Callbask as the message received
client.on('message', function (topic, message) {
    json_message = JSON.parse(message); // convert from text to json
    console.log("=== receive message ===");
    console.log("topic: ", topic.toString());
    console.log("message: ", json_message);
    console.log(json_message.text);

    // Voice Synthesis
    exec("sudo /home/tkr/AquesTalkPi " + json_message.text + "|sudo aplay -D plughw:1", function(err, stdout, stderr){
	/* some process */
    });

});

// Setup keyboard input
process.stdin.resume();
process.stdin.setEncoding('utf8');
var util = require('util');


// Callback when enterkey is pushed
process.stdin.on('data', function (text) {
    text = text.slice(0, -1);  // chop
    console.log('key input data:', util.inspect(text));
    json_message = { 
	"reply": cnf.reply_topic, 
	"text": text,
	"userId": cnf.user_id,
	"timestamp": new Date(),
	"type": "text"
    };
    text_message = JSON.stringify(json_message);
    client.publish(cnf.broker_topic, text_message);
    if (text === 'bye') {
	done();
    }
});


// Julius message arrived
readableStream.on('data', function(text) {
    text = text.slice(0, -1);  // chop
    //console.log('receive:', util.inspect(text));
    text = text.replace( /\s/g ,"");
    console.log('receive:', text);
    json_message = { 
	"reply": cnf.reply_topic, 
	"text": text,
	"userId": cnf.user_id,
	"timestamp": new Date(),
	"type": "text"
    };
    text_message = JSON.stringify(json_message);
    client.publish(cnf.broker_topic, text_message);
});


// Julius process terminated
readableStream.on('end', function() {
    console.log('end');
    process.exit();
});


// Process quit
function done() {
    console.log('end');
    client.end();
    process.exit();
}
