import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
 
class ADS1115:

    def __init__(self, i2c_address=0x48):

        # Initialize the I2C interface
        i2c = busio.I2C(board.SCL, board.SDA)
 
        # Create an ADS1115 object
        ads = ADS.ADS1115(i2c, i2c_address)
 
        # Define the analog input channel
        self.channel0 = AnalogIn(ads, ADS.P0)
        self.channel1 = AnalogIn(ads, ADS.P1)
        self.channel2 = AnalogIn(ads, ADS.P2)
        self.channel3 = AnalogIn(ads, ADS.P3)
    
    def get_channel_0_voltage(self):
        return self.channel0.voltage
    
    def get_channel_1_voltage(self):
        return self.channel1.voltage
    
    def get_channel_2_voltage(self):
        return self.channel2.voltage
    
    def get_channel_3_voltage(self):
        return self.channel3.voltage