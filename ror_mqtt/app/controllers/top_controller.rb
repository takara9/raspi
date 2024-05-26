require 'mqtt/lib'

class TopController < ApplicationController
  def show
    mqtt_init('mqtt://192.155.208.116:1883')
    topic,@power = $client.get('power')
    topic,@pressure = $client.get('pressure')
    topic,@temp_desktop = $client.get('temp_desktop')
    topic,@temp_floor = $client.get('temp_floor')
    topic,@temp_window = $client.get('temp_window')
    topic,@humd_desktop = $client.get('humd_desktop')
    topic,@humd_floor = $client.get('humd_floor')
    topic,@humd_window = $client.get('humd_window')
    mqtt_close()
  end
end
