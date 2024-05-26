#!/usr/bin/env node
//
// MQTT Chat Client
//
// Author : Maho Takara  takara@jp.ibm.com
// 2016/11/26  Initial commit
//

var mqtt    = require('mqtt');
var cnf = require('./etc/client_config.json');
var client  = mqtt.connect(cnf.broker_url);

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

// Process quit
function done() {
    console.log('end');
    client.end();
    process.exit();
}
