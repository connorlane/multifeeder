import serial, sl4824, minimalmodbus, rs485

class Feederbus ( object ):
	def __init__(self, port):
		bus = rs485.RS485(
			48,
			port,
			baudrate = 9600,
			bytesize = serial.SEVENBITS,
			parity = serial.PARITY_EVEN,
			stopbits = serial.STOPBITS_ONE)

		self.heaters = [
			sl4824.sl4824(bus, 4), 
			sl4824.sl4824(bus, 5),
			sl4824.sl4824(bus, 6)
		]

		## DEBUG
		for heater in self.heaters:
			heater.debug = True			



