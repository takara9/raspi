class CreateDeviceSensors < ActiveRecord::Migration
  def change
    create_table :device_sensors do |t|
      t.string :name
      t.string :posision
      t.string :device

      t.timestamps null: false
    end
  end
end
