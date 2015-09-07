import rs485, minimalmodbus, feederbus

bus = feederbus.Feederbus('/dev/ttyO1')

for servo in bus.servos:
	print "ID: " + str(servo.servoId)

#print bus.heaters[0].setPointValue
