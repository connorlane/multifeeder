import serial, sl4824, minimalmodbus, rs485, tsta

class Feederbus ( object ):
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

		## DEBUG ##	
		for servo in self.servos:
			servo.debug = True

		#self.heaters = [
		#	sl4824.sl4824(bus, 4), 
		#	sl4824.sl4824(bus, 5),
		#	sl4824.sl4824(bus, 6)
		#]

		### DEBUG ##
		#for heater in self.heaters:
		#	heater.debug = True			



