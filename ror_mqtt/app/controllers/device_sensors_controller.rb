class DeviceSensorsController < ApplicationController
  before_action :set_device_sensor, only: [:show, :edit, :update, :destroy]

  # GET /device_sensors
  # GET /device_sensors.json
  def index
    @device_sensors = DeviceSensor.all
  end

  # GET /device_sensors/1
  # GET /device_sensors/1.json
  def show
  end

  # GET /device_sensors/new
  def new
    @device_sensor = DeviceSensor.new
  end

  # GET /device_sensors/1/edit
  def edit
  end

  # POST /device_sensors
  # POST /device_sensors.json
  def create
    @device_sensor = DeviceSensor.new(device_sensor_params)

    respond_to do |format|
      if @device_sensor.save
        format.html { redirect_to @device_sensor, notice: 'Device sensor was successfully created.' }
        format.json { render :show, status: :created, location: @device_sensor }
      else
        format.html { render :new }
        format.json { render json: @device_sensor.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /device_sensors/1
  # PATCH/PUT /device_sensors/1.json
  def update
    respond_to do |format|
      if @device_sensor.update(device_sensor_params)
        format.html { redirect_to @device_sensor, notice: 'Device sensor was successfully updated.' }
        format.json { render :show, status: :ok, location: @device_sensor }
      else
        format.html { render :edit }
        format.json { render json: @device_sensor.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /device_sensors/1
  # DELETE /device_sensors/1.json
  def destroy
    @device_sensor.destroy
    respond_to do |format|
      format.html { redirect_to device_sensors_url, notice: 'Device sensor was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_device_sensor
      @device_sensor = DeviceSensor.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def device_sensor_params
      params.require(:device_sensor).permit(:name, :posision, :device)
    end
end
