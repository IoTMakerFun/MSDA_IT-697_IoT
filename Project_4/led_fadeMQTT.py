# Adjust LED brightness by rotating Potentiometer

# GrovePi + Rotary Angle Sensor (Potentiometer) + LED
# http://www.seeedstudio.com/wiki/Grove_-_Rotary_Angle_Sensor
# http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit

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

import time
import grovepi
import paho.mqtt.client as mqtt
import json

# Connect the Rotary Angle Sensor to analog port A2
#potentiometer = 2

# Connect the LED to digital port D5
BLUE_LED = 5

grovepi.pinMode(BLUE_LED, "OUTPUT")
time.sleep(1) # give the hardware time to initialize
i = 0

def on_connect(client, userdata, flags, rc):
	"""Called each time the client connects to the message broker 
	:param client: The client object making the connection
	:param userdata: Arbitrary context specified by the user program
	:param flags: REsponse flags sent by the message broker
	:param rc: the connection result
	:return: None
	"""
	# subscribe to the LEDs topic when connected
	client.subscribe("SNHU/IT697/leds")

def on_message(client, userdata, msg):
	"""Called for each message received
	:param client: The client object making the connection
	:param userdata: Arbitrary context specified by the user program
	:param ms: The message from the MQTT broker
	:return: None
	"""
	print(msg.topic, msg.payload)
	payload = json.loads(msg.payload)
	# the legal values for analogWrite are 0-255
	grovepi.analogWrite(BLUE_LED, payload['blue'])

local_client = mqtt.Client()
local_client.on_connect = on_connect
local_client.on_message = on_message

local_client.connect("localhost")
local_client.loop_forever()



while True:
    try:
        # Read resistance from Potentiometer
        i = grovepi.analogRead(potentiometer)
        print(i)

        # Send PWM signal to LED
        grovepi.analogWrite(led,i//4)

    except IOError:
        print("Error")
