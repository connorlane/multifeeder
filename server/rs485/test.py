import rs485

r = rs485.RS485(48, '/dev/ttyO1')

r.write("Hello, World!")
