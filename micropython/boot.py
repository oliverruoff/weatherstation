import uasyncio as asyncio
from machine import Pin, SoftI2C, WDT
import BME280
from ads1x15 import ADS1115
import network
import json

# Initialize Watchdog Timer
wdt = WDT(timeout=5000)  # Timeout set to 5 seconds

# Connect to WLAN
ssid = 'xxx'
password = 'xxx'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    pass

print('WLAN connected, IP:', wlan.ifconfig()[0])

# Initialize I2C
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)

bme = BME280.BME280(i2c=i2c)
adc = ADS1115(i2c)

# Function to measure and convert to voltage
def read_channel_voltage(channel):
    retry_count = 3
    voltage = 0

    if channel == 0:  # Special case for battery_voltage
        for _ in range(retry_count):
            raw = adc.read(channel1=channel)
            voltage = adc.raw_to_v(raw)
            if voltage != 0:
                break
            asyncio.sleep(0.1)  # Short pause between retries
        if voltage == 0:
            voltage = -1
    else:
        raw = adc.read(channel1=channel)
        voltage = adc.raw_to_v(raw)

    return round(voltage, 2)

# Function to create HTTP response
def create_response(data):
    response = json.dumps(data)
    return 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n' + response

async def handle_request(reader, writer):
    try:
        request_line = await reader.readline()
        print("Request:", request_line)

        while await reader.readline() != b"\r\n":
            pass

        if b"/battery" in request_line:
            voltage = read_channel_voltage(0)
            response = create_response({'battery_voltage': voltage})
        elif b"/solar" in request_line:
            voltage = read_channel_voltage(1)
            response = create_response({'solar_voltage': voltage})
        elif b"/wind" in request_line:
            voltage = read_channel_voltage(2)
            response = create_response({'wind_voltage': voltage})
        elif b"/temperature" in request_line:
            temp = float(bme.temperature.replace('C', '').strip())
            response = create_response({'temperature': round(temp, 2)})
        elif b"/humidity" in request_line:
            hum = float(bme.humidity.replace('%', '').strip())
            response = create_response({'humidity': round(hum, 2)})
        elif b"/pressure" in request_line:
            pres = float(bme.pressure.replace('hPa', '').strip())
            response = create_response({'pressure': round(pres, 2)})
        elif b"/all" in request_line:
            temp = float(bme.temperature.replace('C', '').strip())
            hum = float(bme.humidity.replace('%', '').strip())
            pres = float(bme.pressure.replace('hPa', '').strip())
            battery_voltage = read_channel_voltage(0)
            solar_voltage = read_channel_voltage(1)
            wind_voltage = read_channel_voltage(2)
            response = create_response({
                'temperature': round(temp, 2),
                'humidity': round(hum, 2),
                'pressure': round(pres, 2),
                'battery_voltage': battery_voltage,
                'solar_voltage': solar_voltage,
                'wind_voltage': wind_voltage
            })
        else:
            response = 'HTTP/1.1 404 Not Found\r\n\r\n'
    except Exception as e:
        print("Error handling request:", e)
        response = 'HTTP/1.1 500 Internal Server Error\r\n\r\n'

    await writer.awrite(response)
    await writer.aclose()

async def main():
    while True:
        try:
            server = await asyncio.start_server(handle_request, "0.0.0.0", 80)
            print('Server running...')
            
            # Infinite loop to keep the server running
            while True:
                wdt.feed()  # Feed the Watchdog Timer to prevent reset
                await asyncio.sleep(1)  # Sleep for one second to save resources
                # server remains active during this time
        except Exception as e:
            print("Error in main loop:", e)
            await asyncio.sleep(5)  # Short pause before restarting the server

# Main program
try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass


