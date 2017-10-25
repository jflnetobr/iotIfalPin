#!/usr/bin/python

# this source is part of my Hackster.io project:  https://www.hackster.io/mariocannistra/radio-astronomy-with-rtl-sdr-raspberrypi-and-amazon-aws-iot-45b617

# use this program to test the AWS IoT certificates received by the author
# to participate to the spectrogram sharing initiative on AWS cloud

# this program will publish test mqtt messages using the AWS IoT hub
# to test this program you have to run first its companion awsiotsub.py
# that will subscribe and show all the messages sent by this program

import paho.mqtt.client as paho
import os
import socket
import ssl
import configparser
from time import sleep
from random import *
#from struct import pack

connflag = False

def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
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

mqttc.connect(awshost, awsport, keepalive=300)

mqttc.loop_start()

while 1==1:
    sleep(2)
    if connflag == True:
        #tempreading = 20
        tempreading = uniform(20.1,25.2)
        #tempreading = pack(">H",tempreading)
        mqttc.publish("$aws/things/MeuPrimeiroPikachu/teste", tempreading, qos=0)
        print("msg sent: %f" % tempreading)
    else:
        print("waiting for connection...")
