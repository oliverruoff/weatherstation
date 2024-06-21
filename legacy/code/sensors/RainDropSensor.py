import RPi.GPIO as GPIO

class RainDropSensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def is_raining(self):
        return GPIO.input(self.pin) == 0  # 0 means rain, 1 is dry

    def cleanup(self):
        GPIO.cleanup(self.pin)
