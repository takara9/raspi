def logw(fn,rec)
  fnf = "#{fn}.log"
  if fn == "temp" then
    f = rec.split(",")
    fnf = "#{fn}_#{f[3]}.log"
  end
  File.open(fnf,"a") do |logf|
    logf.puts rec
  end
end
  
def mqtt_init(broker_url)
  $client = MQTT::Client.connect(broker_url)
end

def mqtt_loop()
  $client.get('sensor/#') do |topic,message|
    fn = topic.split("/")
    logw(fn[1],message)
    return message
    break
  end
end
  
def mqtt_close()
  $client.disconnect()
end
