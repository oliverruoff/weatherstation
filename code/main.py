import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
 
# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
 
# Create an ADS1115 object
ads = ADS.ADS1115(i2c)
 
# Define the analog input channel
channel0 = AnalogIn(ads, ADS.P0)
channel1 = AnalogIn(ads, ADS.P0)
channel2 = AnalogIn(ads, ADS.P0)
 
# Loop to read the analog input continuously
while True:
    print("Battery: Analog Value: ", channel0.value, "Voltage: ", channel0.voltage)
    print("Solar: Analog Value: ", channel1.value, "Voltage: ", channel1.voltage)
    print("Wind: Analog Value: ", channel2.value, "Voltage: ", channel2.voltage)
    time.sleep(0.2)