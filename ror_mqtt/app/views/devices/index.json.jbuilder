json.array!(@devices) do |device|
  json.extract! device, :id, :name, :value, :lasttime
  json.url device_url(device, format: :json)
end
