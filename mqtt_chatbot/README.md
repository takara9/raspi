# mqtt_chatbot
MQTT Chatbot with Watson conversation

# How to configure 

~~~
npm install async fs mqtt watson-developer-cloud
~~~

1. rename "mqtt_config.json.sample" to "mqtt_config.json"
2. edit "broker_url" to your MQTT Broker address
3. rename "client_config.json.sample" to "client_config.json"
4. edit "broker_url" to your MQTT Broker address
5. get the credential of IBM Watson Conversation from IBM Bluemix
6. rename "conversation_credentials.json.sample" to "conversation_credentials.json"
7. edit "username" and "password" in "conversation_credentials.json"
8. rename "conversation_workspace_id.json.sample" to "conversation_workspace_id.json"
9. get the workspace id from the tool of IBM Watson Conversation
10. edit "workspace_id" 


# Node.js Files

1. chat_bot.js : The Chatbot based on IBM Watson Conversation and MQTT
2. chat_client.js : Command line client for the Chatbot
3. chat_echo_server.js : Echo server with MQTT 


