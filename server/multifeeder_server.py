import web
import random
import json
import feederbus

bus = feederbus.Feederbus('/dev/ttyO1')

urls = (
    '/', 'index',
    '/(js|css|fonts)/(.*)', 'static',
    '/data', 'data',
	 '/update', 'update'
)

render = web.template.render('templates')

class static:
    def GET(self, media, file):
        try:
		f = open(media+'/'+file, 'r')
		return f.read()
        except:
		raise web.notfound()

class update:
	settings = {
		'feeder1_on' : 'false',
		'feeder2_on' : 'false',
		'feeder3_on' : 'false',
		'heater1_on' : 'false',
		'heater2_on' : 'false',
		'heater3_on' : 'false',
		'feeder1_setpoint' : "0.00",
		'feeder2_setpoint' : "0.00",
		'feeder3_setpoint' : "0.00",
		'heater1_setpoint' : "0.00",
		'heater2_setpoint' : "0.00",
		'heater3_setpoint' : "0.00"
	}

	def POST(self):
		data = web.input()
	
		changed = dict()
		for key in data:
			if key in self.settings:
				if data[key] != self.settings[key]:
					self.settings[key] = changed[key] = data[key]
	
		if 'feeder1_on' in changed:
			bus.feeders[0].runStop = True if changed['feeder1_on'] == 'true' else False
		if 'feeder2_on' in changed:
			bus.feeders[1].runStop = True if changed['feeder2_on'] == 'true' else False
		if 'feeder3_on' in changed:
			bus.feeders[2].runStop = True if changed['feeder3_on'] == 'true' else False
		
		if 'heater1_on' in changed:
			bus.heaters[0].runStop = True if changed['heater1_on'] == 'true' else False
		if 'heater2_on' in changed:
			bus.heaters[1].runStop = True if changed['heater2_on'] == 'true' else False
		if 'heater3_on' in changed:
			bus.heaters[2].runStop = True if changed['heater3_on'] == 'true' else False

		if 'feeder1_setpoint' in changed:
			bus.feeders[0].setPointValue = float(changed['feeder1_setpoint'])
		if 'feeder2_setpoint' in changed:
			bus.feeders[1].setPointValue = float(changed['feeder1_setpoint'])
		if 'feeder3_setpoint' in changed:
			bus.feeders[2].setPointValue = float(changed['feeder1_setpoint'])
		
		if 'heater1_setpoint' in changed:
			bus.heaters[0].setPointValue = float(changed['heater1_setpoint'])
		if 'heater2_setpoint' in changed:
			bus.heaters[1].setPointValue = float(changed['heater2_setpoint'])
		if 'heater3_setpoint' in changed:
			bus.heaters[2].setPointValue = float(changed['heater3_setpoint'])

		return json.dumps(changed)

	def GET(self):
		return json.dumps(self.settings)

class data:
	def GET(self):
		data = {
			'heater1': bus.heaters[0].processValue,
			'heater2': bus.heaters[1].processValue,
			'heater3': bus.heaters[2].processValue,
			'wheel1': random.randint(0, 30),
			'wheel2': random.randint(0, 30),
			'wheel3': random.randint(0, 30)
		}
		
		return json.dumps(data)			

class index:
	def GET(self):
		return render.index()

def setDefaults():
	for heater in bus.heaters:
		heater.onOff = False
		heater.setPointValue = 0
	
	#for servo in bus.servo:
	##	servo.onOff = False
	#	servo.setPointValue = 0
		

if __name__ == "__main__":
	setDefaults()	
	
	app = web.application(urls, globals())
	app.run()

