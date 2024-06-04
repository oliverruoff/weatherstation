from flask import Flask, jsonify
import time
from sensors import ADS1115, BME280, RainDropSensor
import json

# Initialisierung der Sensoren
ads1115 = ADS1115.ADS1115(i2c_address=0x48)
bme280 = BME280.BME280(i2c_address=0x76)
rain_sensor = RainDropSensor.RainDropSensor(pin=18)

# Flask-App initialisieren
app = Flask(__name__)

def format_value(value):
    return round(value, 2)

def get_safe_json(data):
    try:
        return json.dumps(data)
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/battery', methods=['GET'])
def get_battery_voltage():
    voltage = format_value(ads1115.get_channel_0_voltage())
    retry_counter = 0
    while voltage == 0: # this is physically not possible -> system would be dead
        retry_counter += 1
        print('Voltage measurement was 0, trying take another measurement, retry_counter:', retry_counter)
        voltage = format_value(ads1115.get_channel_0_voltage())
        if retry_counter > 3:
            return {'battery_voltage': -1}
    return get_safe_json({'battery_voltage': voltage})

@app.route('/solar', methods=['GET'])
def get_solar_voltage():
    voltage = format_value(ads1115.get_channel_1_voltage())
    retry_counter = 0
    while voltage == 0: # this is physically not possible -> system would be dead
        retry_counter += 1
        print('Voltage measurement was 0, trying take another measurement, retry_counter:', retry_counter)
        voltage = format_value(ads1115.get_channel_1_voltage())
        if retry_counter > 3:
            return {'solar_voltage': -1}
    return get_safe_json({'solar_voltage': voltage})

@app.route('/wind', methods=['GET'])
def get_wind_voltage():
    voltage = format_value(ads1115.get_channel_2_voltage())
    retry_counter = 0
    while voltage == 0: # this is physically not possible -> system would be dead
        retry_counter += 1
        print('Voltage measurement was 0, trying take another measurement, retry_counter:', retry_counter)
        voltage = format_value(ads1115.get_channel_2_voltage())
        if retry_counter > 3:
            return {'wind_voltage': -1}
    return get_safe_json({'wind_voltage': voltage})

@app.route('/bme280', methods=['GET'])
def get_bme280_data():
    bme_data = bme280.get_all()
    return get_safe_json({
        'Temperature': format_value(bme_data.get('temperature', 0)),
        'Pressure': format_value(bme_data.get('pressure', 0)),
        'Humidity': format_value(bme_data.get('humidity', 0))
    })

@app.route('/rain', methods=['GET'])
def get_rain_status():
    if rain_sensor.is_raining():
        return get_safe_json({'Rain Status': 'It is raining.'})
    else:
        return get_safe_json({'Rain Status': 'It is dry.'})

@app.route('/all', methods=['GET'])
def get_all_data():
    battery_voltage = format_value(ads1115.get_channel_0_voltage())
    solar_voltage = format_value(ads1115.get_channel_1_voltage())
    wind_voltage = format_value(ads1115.get_channel_2_voltage())
    bme_data = bme280.get_all()
    rain_status = 'It is raining.' if rain_sensor.is_raining() else 'It is dry.'

    return get_safe_json({
        'battery_voltage': battery_voltage,
        'solar_voltage': solar_voltage,
        'wind_voltage': wind_voltage,
        'temperature': format_value(bme_data.get('temperature', 0)),
        'pressure': format_value(bme_data.get('pressure', 0)),
        'humidity': format_value(bme_data.get('humidity', 0)),
        'rain_status': rain_status
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
