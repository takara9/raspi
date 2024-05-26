# mqtt_chat_node
Minimal Chat Client &amp; Echoback Client by node.js

## How to use this

1. Rename config.json.sample to config.json.
2. Edit "broker_url" to set your MQTT broker address.
3. Execute "chat_echo_server.js" and then it will be waiting the client message.
4. Execute "chat_client.js" and then it will be waiting your input by keyboard.
5. after you input the text to "chat_client.js", it send the MQTT broker and get the echo message by JSON format.


## Why I wrote this code?

This is my programing lesson for a understand how to use MQTT by node.



