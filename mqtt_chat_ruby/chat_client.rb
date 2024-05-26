#!/usr/bin/env ruby 
# encoding: utf-8
#
# MQTT Chat Client
#
# Author : Maho Takara  takara@jp.ibm.com
# 2016/11/26  Initial commit
#

require 'mqtt'
require 'json'

##### MAIN #####
if __FILE__ == $0

  cnf = open("config.json") do |io|
    JSON.load(io)
  end

  print "My reply topic ", cnf['reply_topic'], "\n"

  client = MQTT::Client.connect(cnf['mqtt_broker'])
  client.subscribe( cnf['reply_topic'] )

  while true
    print "> "
    text = gets.chop

    hash_message = {}
    hash_message['text'] = text
    hash_message['reply'] = cnf['reply_topic']
    json_message = JSON.generate(hash_message)

    client.publish( cnf['listen_topic'], json_message, retain=false)

    topic,message = client.get
    puts "#{message}"
  end

  client.disconnect()
end
