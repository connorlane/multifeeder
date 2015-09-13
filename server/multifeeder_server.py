#!/usr/bin/env python

import web
import random
import json
import feederbus
import time
import threading
import atexit

DATA_DIRECTORY = '/srv/multifeeder_server'

bus = feederbus.Feederbus('/dev/ttyO1')
rs485Lock = threading.Lock()

urls = (
    '/', 'index',
    '/(js|css|fonts)/(.*)', 'static',
    '/data', 'data',
	 '/update', 'update'
)

render = web.template.render('/srv/multifeeder_server/templates')

class static:

    def GET(self, media, file):
	p = DATA_DIRECTORY+'/'+media+'/'+file
        try:
		f = open(p, 'r')
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
			if key in update.settings:
				if data[key] != update.settings[key]:
					changed[key] = data[key]

		#try:
		rs485Lock.acquire()
		if 'feeder1_on' in changed:
			bus.servos[0].runStop = True if changed['feeder1_on'] == 'true' else False
		if 'feeder2_on' in changed:
			bus.servos[1].runStop = True if changed['feeder2_on'] == 'true' else False
		if 'feeder3_on' in changed:
			bus.servos[2].runStop = True if changed['feeder3_on'] == 'true' else False
		
		if 'heater1_on' in changed:
			bus.heaters[0].runStop = True if changed['heater1_on'] == 'true' else False
		if 'heater2_on' in changed:
			bus.heaters[1].runStop = True if changed['heater2_on'] == 'true' else False
		if 'heater3_on' in changed:
			bus.heaters[2].runStop = True if changed['heater3_on'] == 'true' else False

		if 'feeder1_setpoint' in changed:
			bus.servos[0].speedCommand = float(changed['feeder1_setpoint'])
		if 'feeder2_setpoint' in changed:
			bus.servos[1].speedCommand = float(changed['feeder2_setpoint'])
		if 'feeder3_setpoint' in changed:
			bus.servos[2].speedCommand = float(changed['feeder3_setpoint'])
		
		if 'heater1_setpoint' in changed:
			bus.heaters[0].setPointValue = float(changed['heater1_setpoint'])
		if 'heater2_setpoint' in changed:
			bus.heaters[1].setPointValue = float(changed['heater2_setpoint'])
		if 'heater3_setpoint' in changed:
			bus.heaters[2].setPointValue = float(changed['heater3_setpoint'])
		rs485Lock.release()

		for key in changed:
			update.settings[key] = changed[key]

		print update.settings

		return json.dumps(changed)

		#except:
			#print "Houston, we have a problem"
			#return web.internalerror("Error writing to internal bus")

	def GET(self):
		return json.dumps(update.settings)

data_dataCache = {}
data_timestamp = 0.0

class data:
	dataCache = {}
	timestamp = 0.0

	DATA_TIMEOUT = 0.75

	def _refreshDataCache(self):
		if data.timestamp < time.time() - self.DATA_TIMEOUT:
			rs485Lock.acquire()
			data.dataCache = {
				'heater1': bus.heaters[0].processValue,
				'heater2': bus.heaters[1].processValue,
				'heater3': bus.heaters[2].processValue,
				'wheel1': bus.servos[0].actualSpeed,
				'wheel2': bus.servos[1].actualSpeed,
				'wheel3': bus.servos[2].actualSpeed
			}	
			rs485Lock.release()
			data.timestamp = time.time()

	def GET(self):
		self._refreshDataCache()

		return json.dumps(data.dataCache)			

class index:
	def GET(self):
		return render.index()

def setDefaults():
	for heater in bus.heaters:
		heater.onOff = False
		heater.setPointValue = 0.0
	
	for servo in bus.servos:
		servo.speedCommand = 0.0
	
@atexit.register
def cleanup_cleanup_everybody_do_your_share():
	bus.servoEnablePin.write(0)

	setDefaults()

if __name__ == "__main__":
	setDefaults()	

	bus.servoEnablePin.write(1)
	
	app = web.application(urls, globals())
	app.run()

