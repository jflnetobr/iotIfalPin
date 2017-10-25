#!/usr/bin/python

# this source is part of my Hackster.io project:  https://www.hackster.io/mariocannistra/radio-astronomy-with-rtl-sdr-raspberrypi-and-amazon-aws-iot-45b617

# use this program to test the AWS IoT certificates received by the author
# to participate to the spectrogram sharing initiative on AWS cloud

# this program will subscribe and show all the messages sent by its companion
# awsiotpub.py using the AWS IoT hub

import paho.mqtt.client as paho
import os
import socket
import ssl
import configparser
from struct import *

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$aws/things/MeuPrimeiroPikachu/teste" , 1 )

def on_message(client, userdata, msg):
    a=msg.payload
    valor=a.decode()
    #print(valor)
    #print("payload: "+str(msg.payload))
    print(valor)
    
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

#def on_log(client, userdata, level, msg):
#    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message
mqttc.on_connect = on_connect

#mqttc.on_log = on_log

cfg = configparser.ConfigParser()
cfg.read('config_files/properties.conf')

awshost = cfg.get('AWS', 'awshost')
awsport = cfg.getint('AWS', 'awsport')
clientId = cfg.get('AWS', 'clientId')
thingName = cfg.get('AWS', 'thingName')
caPath = cfg.get('AWS', 'caPath')
certPath = cfg.get('AWS', 'certPath')
keyPath = cfg.get('AWS', 'keyPath')

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_forever()
