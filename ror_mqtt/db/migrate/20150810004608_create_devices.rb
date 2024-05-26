class CreateDevices < ActiveRecord::Migration
  def change
    create_table :devices do |t|
      t.string :name
      t.integer :value
      t.time :lasttime

      t.timestamps null: false
    end
  end
end
