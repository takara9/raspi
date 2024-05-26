require 'test_helper'

class DeviceSensorsControllerTest < ActionController::TestCase
  setup do
    @device_sensor = device_sensors(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:device_sensors)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create device_sensor" do
    assert_difference('DeviceSensor.count') do
      post :create, device_sensor: { device: @device_sensor.device, name: @device_sensor.name, posision: @device_sensor.posision }
    end

    assert_redirected_to device_sensor_path(assigns(:device_sensor))
  end

  test "should show device_sensor" do
    get :show, id: @device_sensor
    assert_response :success
  end

  test "should get edit" do
    get :edit, id: @device_sensor
    assert_response :success
  end

  test "should update device_sensor" do
    patch :update, id: @device_sensor, device_sensor: { device: @device_sensor.device, name: @device_sensor.name, posision: @device_sensor.posision }
    assert_redirected_to device_sensor_path(assigns(:device_sensor))
  end

  test "should destroy device_sensor" do
    assert_difference('DeviceSensor.count', -1) do
      delete :destroy, id: @device_sensor
    end

    assert_redirected_to device_sensors_path
  end
end
