#!/usr/bin/env node
//
// Chatbot based on IBM Watson conversation
//
//   whenthis code receive a message from MQTT, it 
//   re-send to Watson conversation service and get 
//   the response. and then it reply to MQTT user.
//
//
// Author : Maho Takara  takara@jp.ibm.com
// 2016/11/26  Initial commit
//

var fs = require('fs');
var async = require('async');
var mqtt = require('mqtt');
var cnf = require('./etc/mqtt_config.json');
var bot  = mqtt.connect(cnf.broker_url);


// IBM Watson Conversation
var watson = require('watson-developer-cloud');
var conv_auth = require('./etc/conversation_credentials.json');
var conv_wsid = require('./etc/conversation_workspace_id.json');
var conversation = watson.conversation(conv_auth);

// User session managemnt 
var users = {};

// Folder for downloaded files
const DOWNLOAD = "downloads";

// Floder for logfile
const LOGDIR = "logs";

// MODE  Conversation mode = 0, R&R mode = 1
const CONVERSATION_MODE = 0;
const RR_MODE = 1;
var mode = CONVERSATION_MODE;

// Callback as the connection established                                 
bot.on('connect', function () {
    console.log("connect & subscribe");
    bot.subscribe(cnf.broker_topic);
});

// Getting a message
bot.on('message', function (topic, message) {
    json_message = JSON.parse(message);
    console.log("=== receive message ===");
    console.log("topic: ", topic.toString());
    console.log("message: ", json_message);

    id = json_message.userId;
    time = new Date();

    async.series([
	function(callback) {
	    if (users[id] == undefined ) {
		users[id] = { 
		    profile: {},
		    response: {},
		    count: 0,
		    start_time: time,
		    last_time: time
		};
		callback(null);
	    } else {
		callback(null);
	    }
	}],function(err, results) {
	    users[id].count = users[id].count + 1;
	    users[id].last_time = time;
	    eventHandler(json_message,users[id]);
	});
});

// JSON log writer
function jsonLogWriter(json_data) {
    text_data = JSON.stringify(json_data, null, 2);
    text_data = text_data + "\n"
    console.log(text_data);
    fpath = LOGDIR + "/" + "chat_log.txt"
    fs.appendFileSync(fpath, text_data ,'utf8');
}


// Chatbot main 
function eventHandler(msg,user_handler) {

    //console.log("mode = ", user_handler.mode);
    if (user_handler.mode == RR_MODE) {
	json_reply = { "text" : "この機能は実装されていません"};
	text_message = JSON.stringify(json_reply);
	bot.publish(msg.reply, text_message);
	jsonLogWriter(user_handler);
	user_handler.mode = CONVERSATION_MODE;
	user_handler.response.context.conversation_id = "";
	return;
    }


    if (msg.type == 'text') {
	console.log("Message ----");

	// Call Watson conversation 
	conversation.message({
	    workspace_id: conv_wsid.workspace_id,
	    input: {'text': msg.text},
	    context: user_handler.response.context
	},function(err, response) {
	    if (err) {
		console.log('error:', err);
	    }
	    else {
		user_handler.response = response;
		var textMsg = "";
		for(i = 0; i < response.output.text.length; i++) {
		    textMsg = textMsg + " " + response.output.text[i];
		}
		
		json_reply = { "text" : textMsg};
		text_message = JSON.stringify(json_reply);
		bot.publish(msg.reply, text_message);
		jsonLogWriter(user_handler);
		
		// Change to Watson R&R mode
		if (response.context.watson_rr == true ) {
		    user_handler.mode = RR_MODE;
		}
	    }
	});

    } else if (msg.type == 'image') {
	console.log("Image ----");
    } else if (msg.type == 'audio') {
	console.log("Sound ----");
	console.log("The sound file is saved at ", fpath);
    } else if (msg.type == 'sticker') {
	console.log("Sticker ----");
    } else {
	console.log("Other ----");
    }
}





