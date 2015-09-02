import serial, sl4824, minimalmodbus, rs485

class Feederbus ( object ):
	def __init__(self, port):

		self.heaters = [
			sl4824.sl4824(port, 4), 
			sl4824.sl4824(port, 5),
			sl4824.sl4824(port, 6)
		]

		## DEBUG
		for heater in self.heaters:
			heater.debug = True			

		rs485.setupRS485(self.heaters[0].serial, 48)

