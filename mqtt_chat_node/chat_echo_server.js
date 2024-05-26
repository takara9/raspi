#!/usr/bin/env node
//
// MQTT Chat loopback test server
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
    client.subscribe(cnf.broker_topic);
});

// Callbask as the message received
client.on('message', function (topic, message) {
    console.log("=== receive message ===");
    console.log("topic: ", topic.toString());
    console.log("message: ", message.toString());
    // convert from text to json
    json_message = JSON.parse(message);
    console.log(json_message);
    client.publish(json_message.reply, message.toString());
});

