import time
from sensors import ADS1115, BME280

ads1115 = ADS1115.ADS1115(i2c_address=0x48)
bme280 = BME280.BME280(i2c_address=0x76)

# Loop to read the analog input continuously
while True:
    print("Battery Voltage: ", ads1115.get_channel_0_voltage())
    print("Solar Voltage: ", ads1115.get_channel_1_voltage())
    print("Wind Voltage: ", ads1115.get_channel_2_voltage())
    bme_data = bme280.get_all()
    print(bme_data)
    print("__________________________________________________________________")
    time.sleep(1)