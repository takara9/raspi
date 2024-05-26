json.array!(@device_sensors) do |device_sensor|
  json.extract! device_sensor, :id, :name, :posision, :device
  json.url device_sensor_url(device_sensor, format: :json)
end
