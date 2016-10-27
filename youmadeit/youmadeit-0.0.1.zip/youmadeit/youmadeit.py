#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import json
import urllib
import base64

class YouMadeIt:
	apiKey = ""
	deviceName = ""
	encodedDeviceName = ""
	client = None
	onReceiveCallbackFunction = None
	subscribeTopic = ""

	def __init__(self, apiKey, deviceName="noName"):
		self.apiKey = apiKey
		self.deviceName = deviceName
		self.encodedDeviceName = self._encode(deviceName)

		client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
		self.client = client

		client.on_connect = self.__on_connect
		client.on_message = self.__on_message

		#client.connect("localhost", 1883, 60)
		client.connect("37.187.109.185", 1883, 60)

		# Non blocking call that processes network traffic, dispatches callbacks and
		# handles reconnecting.
		# Other loop*() functions are available, see the manual.
		client.loop_start()

	# Encode using urlencode format (escape special chars with %xx format)
	def _encode(self, str):
		return urllib.quote(str, safe='')

	# The callback for when the client receives a CONNACK response from the server.
	def __on_connect(self, client, userdata, flags, rc):
	    print("Connected with result code "+str(rc))

	    # Subscribing in on_connect() means that if we lose the connection and
	    # reconnect then subscriptions will be renewed.
	    # client.subscribe("$SYS/#")

	    # Set the topic to subscribe to
	    subscribeTopic = u"client/" + self.apiKey + "/" + self.encodedDeviceName
	    print "Encoded device name : ", self.encodedDeviceName
	    self.subscribeTopic = subscribeTopic
	    client.subscribe(subscribeTopic, qos=0)
	    # Test publication - Do not forget to put 'u' before a unicode string
	    # client.publish("coucou/mytopic", payload=u"voilà mon message", qos=0, retain=False)

	# The callback for when a PUBLISH message is received from the server.
	def __on_message(self, client, userdata, msg):
	    # print(msg.topic+" "+str(msg.payload))
	    data = json.loads(msg.payload)
	    paramName = data['paramName']
	    value = data['data']
	    self.onReceiveCallbackFunction(paramName, value, data)

	# Defines which function to callback when a message is received
	def onReceive(self, callbackFunction):
		self.onReceiveCallbackFunction = callbackFunction

	# Send data to mobile app through broker
	def sendToMobile(self, paramName, data, subtitle=None):
		topic = "mobile" + "/" + self.apiKey
		dataType = 'num' if isinstance(data, (int, long, float)) else 'str'
		payloadJson = {
			'deviceName': self.deviceName,
			'paramName': paramName,
			'dataType': dataType,
			'data': data
		}
		if subtitle is not None:
			payloadJson['subtitle'] = subtitle
		# ensure_ascii=False prevents json.dumps from escaping unicode with \u
		payload = json.dumps(payloadJson)
		self.client.publish(topic, payload, qos=0, retain=False)

	# Send data to mobile app through broker
	def sendImageToMobile(self, paramName, data, imageType, subtitle=None):
		topic = "mobile" + "/" + self.apiKey
		dataType = 'img'
		base64image = 'data:image/' + imageType + ';base64,' + base64.b64encode(data)
		payloadJson = {
			'deviceName': self.deviceName,
			'paramName': paramName,
			'dataType': dataType,
			'data': base64image
		}
		if subtitle is not None:
			payloadJson['subtitle'] = subtitle
		# ensure_ascii=False prevents json.dumps from escaping unicode with \u
		payload = json.dumps(payloadJson)
		self.client.publish(topic, payload, qos=0, retain=False)

	# Send data to other device through broker
	def sendToDevice(self, targetDeviceName, paramName, data):
		encodedTargetDeviceName = self._encode(targetDeviceName)
		topic = "client/" + self.apiKey + "/" + encodedTargetDeviceName
		print topic
		dataType = 'num' if isinstance(data, (int, long, float)) else 'str'
		payloadJson = {
			'deviceName': self.deviceName,
			'paramName': paramName,
			'dataType': dataType,
			'data': data
		}
		# ensure_ascii=False prevents json.dumps from escaping unicode with \u
		payload = json.dumps(payloadJson)
		self.client.publish(topic, payload, qos=0, retain=False)

