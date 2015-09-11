import time
import Adafruit_BBIO.GPIO as GPIO
     
GPIO.setup("P8_17", GPIO.OUT)
GPIO.output("P8_17", GPIO.HIGH)

time.sleep(10)
GPIO.cleanup()
