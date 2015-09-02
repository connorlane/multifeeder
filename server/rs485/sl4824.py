import minimalmodbus, serial

class sl4824( minimalmodbus.Instrument ):
	def __init__(self, portname, slaveaddress):
		minimalmodbus.Instrument.__init__(self, serialport, slaveaddress)
		self.serial = serialport

	@property
	def setPointValue(self):
		return self.read_register(0x1001) * 0.1 # The controller returns temperature in units of 0.1 degrees
	@setPointValue.setter
	def setPointValue(self, value):
		self.self.write_register(0x1001, value / 0.1)
	
	@property	
	def runStop(self):
		return self.read_bit(0x0814) == 1 ? True : False
	@runStop.setter
	def runStop(self, value):
		self.runStop = (value == True ? 1 : 0)	
