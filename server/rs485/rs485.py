import serial, fcntl, struct

class RS485(serial.Serial):
	def __init__(self, port=None, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, writeTimeout=None, dsrdtr=False, interCharTimeout=None):
		serial.Serial.__init__(self, port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts, writeTimeout, dsrdtr, interCharTimeout)

		# Standard Linux RS485 ioctl:
		TIOCSRS485 = 0x542F
		 
		# define serial_rs485 struct per Michael Musset's patch that adds gpio RE/DE 
		# control:
		# (https://github.com/RobertCNelson/bb-kernel/blob/am33x-v3.8/patches/fixes/0007-omap-RS485-support-by-Michael-Musset.patch#L30)
		SER_RS485_ENABLED         = (1 << 0)
		SER_RS485_RTS_ON_SEND     = (1 << 1)
		SER_RS485_RTS_AFTER_SEND  = (1 << 2)
		SER_RS485_RTS_BEFORE_SEND = (1 << 3)
		SER_RS485_USE_GPIO        = (1 << 5)
		 
		# Enable RS485 mode using a GPIO pin to control RE/DE: 
		RS485_FLAGS = SER_RS485_ENABLED | SER_RS485_USE_GPIO 
		# With this configuration the GPIO pin will be high when transmitting and low
		# when not
		 
		# If SER_RS485_RTS_ON_SEND and SER_RS485_RTS_AFTER_SEND flags are included the
		# RE/DE signal will be inverted, i.e. low while transmitting
		 
		# The GPIO pin to use, using the Kernel numbering: 
		RS485_RTS_GPIO_PIN = 48 # GPIO1_16 -> GPIO(1)_(16) = (1)*32+(16) = 48
		 
		# Pack the config into 8 consecutive unsigned 32-bit values:
		# (per  struct serial_rs485 in patched serial.h)
		serial_rs485 = struct.pack('IIIIIIII', 
											RS485_FLAGS,        # config flags
											0,                  # delay in us before send
											0,                  # delay in us after send
											RS485_RTS_GPIO_PIN, # the pin number used for DE/RE
											0, 0, 0, 0          # padding - space for more values 
											)
		 
		# Apply the ioctl to the open ttyO4 file descriptor:
		fd=self.fileno()
		fcntl.ioctl(fd, TIOCSRS485, serial_rs485)


