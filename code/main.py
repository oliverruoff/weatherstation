import time
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create BME280 object
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# Optionally, you can change the sensor's address (default is 0x77)
# bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# Change the sea level pressure at your location (hPa)
bme280.sea_level_pressure = 1013.25

def read_bme280():
    temperature = bme280.temperature
    humidity = bme280.humidity
    pressure = bme280.pressure
    return temperature, humidity, pressure

def main():
    while True:
        temperature, humidity, pressure = read_bme280()
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Humidity: {humidity:.2f} %")
        print(f"Pressure: {pressure:.2f} hPa")
        time.sleep(2)

if __name__ == "__main__":
    main()