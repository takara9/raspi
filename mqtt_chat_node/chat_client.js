#!/usr/bin/env node
//
// MQTT Chat Client
//
// Author : Maho Takara  takara@jp.ibm.com
// 2016/11/26  Initial commit
//

var mqtt    = require('mqtt');
var cnf = require('./config.json');
var client  = mqtt.connect(cnf.broker_url);

// Callback as the connection established
client.on('connect', function () {
    console.log("connect & subscribe");
    client.subscribe(cnf.reply_topic);
});

// Callbask as the message received
client.on('message', function (topic, message) {
    console.log("=== receive message ===");
    console.log("topic: ", topic.toString());
    console.log("message: ", message.toString());
});

// Setup keyboard input
process.stdin.resume();
process.stdin.setEncoding('utf8');
var util = require('util');

// Callback when enterkey is pushed
process.stdin.on('data', function (text) {
    text = text.slice(0, -1);  // chop
    console.log('key input data:', util.inspect(text));
    json_message = { "reply": cnf.reply_topic, "text": text};
    text_message = JSON.stringify(json_message, null, 0);
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
