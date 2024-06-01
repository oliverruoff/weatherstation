import time
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.ads1x15 import ADS

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize BME280 sensor
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# Initialize ADS1115
ads = ADS1115(i2c)
chan0 = AnalogIn(ads, ADS.P0)  # Battery voltage
chan1 = AnalogIn(ads, ADS.P1)  # Solar panel voltage
chan2 = AnalogIn(ads, ADS.P2)  # Wind motor voltage

# Change the sea level pressure at your location (hPa)
bme280.sea_level_pressure = 1013.25

def read_bme280():
    temperature = bme280.temperature
    humidity = bme280.humidity
    pressure = bme280.pressure
    return temperature, humidity, pressure

def read_ads1115():
    battery_voltage = chan0.voltage
    solar_panel_voltage = chan1.voltage
    wind_motor_voltage = chan2.voltage
    return battery_voltage, solar_panel_voltage, wind_motor_voltage

def main():
    while True:
        temperature, humidity, pressure = read_bme280()
        battery_voltage, solar_panel_voltage, wind_motor_voltage = read_ads1115()
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Humidity: {humidity:.2f} %")
        print(f"Pressure: {pressure:.2f} hPa")
        print(f"Battery Voltage: {battery_voltage:.2f} V")
        print(f"Solar Panel Voltage: {solar_panel_voltage:.2f} V")
        print(f"Wind Motor Voltage: {wind_motor_voltage:.2f} V")
        time.sleep(2)

if __name__ == "__main__":
    main()
