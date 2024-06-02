import smbus2
import bme280

class BME280:
    def __init__(self, i2c_address=0x76, i2c_bus=1):
        self.bus = smbus2.SMBus(i2c_bus)
        self.address = i2c_address
        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)
        self.data = None
    
    def update(self):
        self.data = bme280.sample(self.bus, self.address, self.calibration_params)
    
    def get_temperature(self):
        self.update()
        return self.data.temperature
    
    def get_pressure(self):
        self.update()
        return self.data.pressure
    
    def get_humidity(self):
        self.update()
        return self.data.humidity
    
    def get_all(self):
        self.update()
        return {
            'temperature': self.data.temperature,
            'pressure': self.data.pressure,
            'humidity': self.data.humidity
        }

