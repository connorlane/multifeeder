import rs485, minimalmodbus, feederbus

bus = feederbus.Feederbus('/dev/ttyO1')

try:
	bus.heaters[0].setPointValue = 300
except:
	pass

bus.heaters[1].setPointValue = 20
