import web
import random
import json

#DEBUG
import datetime
web.config.debug = True
#/DEBUG

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
		
		print data

		changed = dict()
		for key in self.settings:
			if key in data:
				changed[key] = self.settings[key] = data[key]
				print "Updated " + str(key)
			
		print json.dumps(changed)

		return json.dumps(changed)

	def GET(self):
		return json.dumps(self.settings)
		

class data:
	def GET(self):
		data = {
			'heater1': random.randint(1, 200),
			'heater2': random.randint(1, 200),
			'heater3': random.randint(1, 200),
			'wheel1': random.randint(0,  30),
			'wheel2': random.randint(0,  30),
			'wheel3': random.randint(0,  30)
		}
		
		return json.dumps(data)			

class index:
    def GET(self):
		return render.index()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

