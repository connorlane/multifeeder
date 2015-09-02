import serial, rs485

feederbus = rs485.RS485(port='/dev/ttyUSB0', baudrate=9600, timeout=1, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, bytesize=serial.SEVENBITS);

#heater1 = sl4824.sl4824(, 4)
#heater1.mode = minimalmodbus.MODE_ASCII
#heater1.debug = True

#print heater1.write_register(0x1001, 1400)

 
