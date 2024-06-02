import time
import RPi.GPIO as GPIO
from sensors import ADS1115, BME280, RainDropSensor

# Setup for the rain sensor
RAIN_SENSOR_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(RAIN_SENSOR_PIN, GPIO.IN)

ads1115 = ADS1115.ADS1115(i2c_address=0x48)
bme280 = BME280.BME280(i2c_address=0x76)
rain_sensor = RainDropSensor.RainDropSensor(pin=18)

# Function to read rain sensor
def is_raining():
    return GPIO.input(RAIN_SENSOR_PIN) == 1

# Loop to read the analog input continuously
while True:
    print("Battery Voltage: ", ads1115.get_channel_0_voltage())
    print("Solar Voltage: ", ads1115.get_channel_1_voltage())
    print("Wind Voltage: ", ads1115.get_channel_2_voltage())
    
    bme_data = bme280.get_all()
    print("Temperature: {:.2f} C".format(bme_data['temperature']))
    print("Pressure: {:.2f} hPa".format(bme_data['pressure']))
    print("Humidity: {:.2f} %".format(bme_data['humidity']))
    
    if rain_sensor.is_raining():
        print("Rain Status: It is raining.")
    else:
        print("Rain Status: It is dry.")
    
    print("__________________________________________________________________")
    time.sleep(1)
