import serial
from drivers import sl4824, minimalmodbus, rs485, tsta, beaglebonegpio

class Feederbus ( object ):
	SERVO_ENABLE_PIN_NUMBER = 27

	def __init__(self, port):
		bus = rs485.RS485(
			49,
			port,
			baudrate = 9600,
			bytesize = serial.SEVENBITS,
			parity = serial.PARITY_EVEN,
			stopbits = serial.STOPBITS_ONE)

		self.servos = [
			tsta.TSTA(bus, 1),
			tsta.TSTA(bus, 2),
			tsta.TSTA(bus, 3)
		]

		self.heaters = [
			sl4824.sl4824(bus, 4), 
			sl4824.sl4824(bus, 5),
			sl4824.sl4824(bus, 6)
		]

		## Uncomment for debug messages on the RS485 bus ##
		#for heater in self.heaters:
		#	heater.debug = True

		#for servo in self.servos:
		#	servo.debug = True

		self.servoEnablePin = beaglebonegpio.BeagleBoneGPIO(Feederbus.SERVO_ENABLE_PIN_NUMBER)
