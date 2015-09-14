import minimalmodbus, serial

class TSTA( minimalmodbus.Instrument, object ):
	SERVO_ID_REGISTER = 0x0024
	ACTUAL_SPEED_REGISTER = 0x0601
	SPEED_COMMAND_REGISTER = 0x0201

	speedCommandSetting = 0.0
	runStopSetting = False

	def __init__(self, port, slaveaddress):
		minimalmodbus.Instrument.__init__(self, port, slaveaddress)
		#self.serial.bytesize = serial.SEVENBITS
		#self.serial.baudrate = 9600
		#self.serial.timeout = 1
		#self.serial.parity = serial.PARITY_NONE
		#self.serial.stopbits = serial.STOPBITS_TWO
		self.mode = minimalmodbus.MODE_ASCII

	## servoId - Get the current servo id ##
	@property
	def servoId(self):
		return self.read_register(self.SERVO_ID_REGISTER)


	## actualSpeed - Get the actual current motor speed ##
	@property
	def actualSpeed(self):
		return self.read_register(self.ACTUAL_SPEED_REGISTER)


	## speedCommand - Get/set the speed command value ##
	@property
	def speedCommand(self):
		return self.read_register(self.SPEED_COMMAND_REGISTER)


	@speedCommand.setter
	def speedCommand(self, value):
		self.speedCommandSetting = value
		if self.runStopSetting:
			self.write_register(self.SPEED_COMMAND_REGISTER, value)

	## runStop - Turn the feeder on or off ##

	@property	
	def runStop(self):
		return self.runStopSetting

	@runStop.setter
	def runStop(self, value):
		if value:
			print "Setting to " + str(self.speedCommandSetting)
			self.write_register(self.SPEED_COMMAND_REGISTER, self.speedCommandSetting)
		else:
			self.write_register(self.SPEED_COMMAND_REGISTER, 0.0)

		self.runStopSetting = value

