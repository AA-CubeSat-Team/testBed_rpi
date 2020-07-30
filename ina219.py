
import board
import busio
import adafruit_ina219 

i2c = busio.I2C(board.SCL, board.SDA) 
sensor = adafruit_ina219.INA219(i2c)

print("Bus Voltage: {} V".format(sensor.bus_voltage)) 
print("Shunt Voltage: {} mV".format(sensor.shunt_voltage / 1000)) 
print("Current: {} mA".format(sensor.current))