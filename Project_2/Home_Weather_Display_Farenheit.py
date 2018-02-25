# Home_Weather_Display.py
#
# This is an project for using the Grove RGB LCD Display and the Grove DHT Sensor from the GrovePi starter kit
#
# In this project, the Temperature and humidity from the DHT sensor is printed on the RGB-LCD Display
#
#
# Note the dht_sensor_type below may need to be changed depending on which DHT sensor you have:
#  0 - DHT11 - blue one - comes with the GrovePi+ Starter Kit
#  1 - DHT22 - white one, aka DHT Pro or AM2302
#  2 - DHT21 - black one, aka AM2301
#
# For more info please see: http://www.dexterindustries.com/topic/537-6c-displayed-in-home-weather-project/
#
'''
The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from grovepi import *
from grove_rgb_lcd import *
from time import sleep
from math import isnan

import paho.mqtt.client as mqtt

import json

dht_sensor_port = 7 # connect the DHt sensor to port 7
dht_sensor_type = 0 # use 0 for the blue-colored sensor and 1 for the white-colored sensor

# set green as backlight color
# we need to do it just once
# setting the backlight color once reduces the amount of data transfer over the I2C line
setRGB(0,255,0)

local_client = mqtt.Client()
local_client.connect("localhost")
local_client.loop_start()

remote_client = mqtt.Client()
remote_client.connect("test.mosquitto.org")
remote_client.loop_start()

while True:
	try:
        # get the temperature and Humidity from the DHT sensor
		[ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)
		temp = temp * 9.0 / 5.0 + 32.0

		if math.isnan(temp):
#			print("temp is not a number")
			continue
		if math.isnan(hum):
#			print("hum is not a num")
			continue

#		print("temp =" + temp + "F\thumidity =" + hum + "%")
		send_string = "temp =" + str(temp) + "F\thumidity =" + str(hum) + "%"

# Need to build python dictionary instead of send_string
		send_string_dict = {}

		send_string_data_dict = {}
		send_string_data_dict["humidity"] = hum
		send_string_data_dict["temperature"] = temp

		send_string_dict["data"] = send_string_data_dict
		send_string_dict["timestamp"] = time.time()
		send_string_dict["email"] = "javageek at gmail"

		send_string_json = json.dumps(send_string_dict)

		print(send_string_dict)

#		local_client.publish("hello/world", send_string)
#		local_client.publish("SNHU/IT697/sensor/data/json", send_string)
		local_client.publish("SNHU/IT697/sensor/data/json", send_string_json)
		remote_client.publish("SNHU/IT697/sensor/data/json", send_string_json)


		# check if we have nans
		# if so, then raise a type error exception
		if isnan(temp) is True or isnan(hum) is True:
			raise TypeError('nan error')

		t = str(temp)
		h = str(hum)

        # instead of inserting a bunch of whitespace, we can just insert a \n
        # we're ensuring that if we get some strange strings on one line, the 2nd one won't be affected
		setText_norefresh("Temp:" + t + "C\n" + "Humidity :" + h + "%")

	except (IOError, TypeError) as e:
		print(str(e))
		# and since we got a type error
		# then reset the LCD's text
		setText("")

	except KeyboardInterrupt as e:
		print(str(e))
		# since we're exiting the program
		# it's better to leave the LCD with a blank text
		setText("")
		break

	# wait some time before re-updating the LCD
	sleep(0.05)
