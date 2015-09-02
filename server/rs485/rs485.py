import serial, fcntl, struct, time, minimalmodbus

heater1 = minimalmodbus.Instrument('/dev/ttyO1', 4)
heater1.mode = minimalmodbus.MODE_ASCII
heater1.debug = True

heater1.serial.baudrate = 9600
heater1.serial.timeout = 1
heater1.serial.parity = serial.PARITY_EVEN
heater1.serial.stopbits = serial.STOPBITS_ONE
heater1.serial.bytesize = serial.SEVENBITS
 
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
fd=heater1.serial.fileno()
fcntl.ioctl(fd, TIOCSRS485, serial_rs485)

print heater1.write_register(0x1001, 1400)
print heater1.write_bit(0x814, 0)

 
