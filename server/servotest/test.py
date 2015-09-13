import time
import Adafruit_BBIO.GPIO as GPIO
from drivers import tsta, beaglebonegpio

servoEnablePin = beaglebonegpio.BeagleBoneGPIO(27)     

time.sleep(5)

servoEnablePin.write(1)

bus = rs485.RS485(
	49,
	'/dev/ttyO1',
	baudrate = 9600,
	bytesize = serial.SEVENBITS,
	parity = serial.PARITY_EVEN,
	stopbits = serial.STOPBITS_ONE)

s = tsta.TSTA(bus, 1)

s.debug = True

s.speedCommand = 5.0

time.sleep(5)

servoEnablePin.write(0)
