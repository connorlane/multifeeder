import os 
class BeagleBoneGPIO:
	def __init__(self,gpio_pin):
		self.gpio_pin = gpio_pin
		os.system("echo %d > /sys/class/gpio/export" % self.gpio_pin)
		self.gpio_path = "/sys/class/gpio/gpio%d/"%gpio_pin
		with open(self.gpio_path+"direction") as f:
			self.direction = f.read()

	def write(self,value):
		if self.direction != "out":
			os.system("echo out > %sdirection"%self.gpio_path)
		self.direction = "out"
		os.system("echo %s > %svalue"%(value,self.gpio_path))

	def read(self):
		if self.direction != "in":
			os.system("echo in > %sdirection"%self.gpio_path)
		self.direction = "in"
		with open(self.gpio_path+value) as f:
			return f.read()
