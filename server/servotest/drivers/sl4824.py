import minimalmodbus, serial

class sl4824( minimalmodbus.Instrument, object ):
	PROCESSVALUE_REGISTER = 0x1000
	SETPOINTVALUE_REGISTER = 0x1001
	RUNSTOP_REGISTER = 0x0814

	def __init__(self, port, slaveaddress):
		minimalmodbus.Instrument.__init__(self, port, slaveaddress)
		self.serial.bytesize = serial.SEVENBITS
		self.serial.baudrate = 9600
		self.serial.timeout = 1
		self.serial.parity = serial.PARITY_EVEN
		self.serial.stopbits = serial.STOPBITS_ONE
		self.mode = minimalmodbus.MODE_ASCII


	## setPointValue - Set/Get current temperature target ##
	@property
	def setPointValue(self):
		return self.read_register(self.SETPOINTVALUE_REGISTER) * 0.1 # The controller returns temperature in units of 0.1 degrees

	@setPointValue.setter
	def setPointValue(self, value):
		self.write_register(self.SETPOINTVALUE_REGISTER, value / 0.1)


	## runStop - Turn the heater on or off ##

	@property	
	def runStop(self):
		return True if self.read_bit(self.RUNSTOP_REGISTER) == 1 else False

	@runStop.setter
	def runStop(self, value):
		 self.write_bit(self.RUNSTOP_REGISTER, 1 if value else 0)

	@property
	def processValue(self):
		pv = self.read_register(self.PROCESSVALUE_REGISTER)
		if pv != 0x8002 and pv != 0x8003 and pv != 0x8004 and pv != 0x8006 and pv != 0x8007:
			return pv * 0.1
		else:
			return 0
