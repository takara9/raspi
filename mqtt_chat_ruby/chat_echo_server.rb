#!/usr/bin/env ruby 
# encoding: utf-8
#
# MQTT Echo back server
# 
# Author : Maho Takara  takara@jp.ibm.com
# 2016/11/26  Initial commit

require 'mqtt'
require 'json'


def mqtt_loop(client,cnf)
  client.get(cnf['listen_topic']) do |topic,message|
    puts "#{topic},#{message}"
    
    hash_message = JSON.parse(message)
    print "hash reply = ", hash_message['reply'],"\n"
    client.publish(bash_message['reply'], message, retain=false)
  end
end


##### MAIN #####
if __FILE__ == $0

  cnf = open("config.json") do |io|
    JSON.load(io)
  end

  client = MQTT::Client.connect(cnf['mqtt_broker'])
  print "waiting message\n"
  mqtt_loop(client,cnf)
  client.disconnect()

end
