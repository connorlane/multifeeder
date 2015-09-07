import minimalmodbus, serial

class TSTA( minimalmodbus.Instrument, object ):
	SERVO_ID_REGISTER = 0x0024

	def __init__(self, port, slaveaddress):
		minimalmodbus.Instrument.__init__(self, port, slaveaddress)
		self.serial.bytesize = serial.SEVENBITS
		self.serial.baudrate = 9600
		self.serial.timeout = 1
		self.serial.parity = serial.PARITY_NONE
		self.serial.stopbits = serial.STOPBITS_TWO
		self.mode = minimalmodbus.MODE_ASCII

	## servoId - Get the current servo id ##
	@property
	def servoId(self):
		return self.read_register(self.SERVO_ID_REGISTER)
