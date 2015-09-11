import minimalmodbus, serial

class TSTA( minimalmodbus.Instrument, object ):
	SERVO_ID_REGISTER = 0x0024
	CONTROL_MODE_REGISTER = 0x0001

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

	## Control Mode ##
	class ControlMode(object):
		TORQUE = 0,
		SPEED = 1,
		EXTERNAL_PULSE = 2,
		POSITION_SPEED = 3,
		SPEED_TORQUE = 4,
		POSITION_TORQUE = 5,
		INTERNAL_POSITION = 6

	@property
	def controlMode(self):
		return self.read_register(self.CONTROL_MODE_REGISTER)

	@controlMode.setter
	def controlMode(self, value):
		self.write_register(self.CONTROL_MODE_REGISTER, value)

	
