from flask import Flask, jsonify
import time
from sensors import ADS1115, BME280, RainDropSensor

# Initialisierung der Sensoren
ads1115 = ADS1115.ADS1115(i2c_address=0x48)
bme280 = BME280.BME280(i2c_address=0x76)
rain_sensor = RainDropSensor.RainDropSensor(pin=18)

# Flask-App initialisieren
app = Flask(__name__)

@app.route('/battery', methods=['GET'])
def get_battery_voltage():
    voltage = ads1115.get_channel_0_voltage()
    return jsonify({'Battery Voltage': voltage})

@app.route('/solar', methods=['GET'])
def get_solar_voltage():
    voltage = ads1115.get_channel_1_voltage()
    return jsonify({'Solar Voltage': voltage})

@app.route('/wind', methods=['GET'])
def get_wind_voltage():
    voltage = ads1115.get_channel_2_voltage()
    return jsonify({'Wind Voltage': voltage})

@app.route('/bme280', methods=['GET'])
def get_bme280_data():
    bme_data = bme280.get_all()
    return jsonify({
        'Temperature': bme_data['temperature'],
        'Pressure': bme_data['pressure'],
        'Humidity': bme_data['humidity']
    })

@app.route('/rain', methods=['GET'])
def get_rain_status():
    if rain_sensor.is_raining():
        return jsonify({'Rain Status': 'It is raining.'})
    else:
        return jsonify({'Rain Status': 'It is dry.'})

@app.route('/all', methods=['GET'])
def get_all_data():
    battery_voltage = ads1115.get_channel_0_voltage()
    solar_voltage = ads1115.get_channel_1_voltage()
    wind_voltage = ads1115.get_channel_2_voltage()
    bme_data = bme280.get_all()
    rain_status = 'It is raining.' if rain_sensor.is_raining() else 'It is dry.'

    return jsonify({
        'Battery Voltage': battery_voltage,
        'Solar Voltage': solar_voltage,
        'Wind Voltage': wind_voltage,
        'Temperature': bme_data['temperature'],
        'Pressure': bme_data['pressure'],
        'Humidity': bme_data['humidity'],
        'Rain Status': rain_status
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)