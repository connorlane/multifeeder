import feederbus

bus = feederbus.Feederbus('/dev/ttyO1')

for heater in bus.heaters:
	print heater.setPointValue

for servo in bus.servos:
	print "ID: " + str(servo.servoId)

#print bus.heaters[0].setPointValue
