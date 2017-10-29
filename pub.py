'''
This source is part of:
https://www.hackster.io/mariocannistra/radio-astronomy-with-rtl-sdr-raspberrypi-and-amazon-aws-iot-45b617

Use this program to test the AWS IoT certificates received by the author
to participate to the spectrogram sharing initiative on AWS cloud

This program will publish test mqtt messages using the AWS IoT hub
to test this program you have to run first its companion awsiotsub.py
that will subscribe and show all the messages sent by this program
'''

# Importações
import paho.mqtt.client as paho
import os
import socket
import ssl
import configparser
from time import sleep
from random import *
connflag = False

# Definição de funções
# Ao conectar
def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )

# Ao receber mensagem
def on_message(client, userdata, msg):
    print(msg.payload.decode())

# Chamadas de função
mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Lendo o arquivo de propriedades e obtendo os valores
prop = configparser.ConfigParser()
prop.read('config_files/properties.conf')

# Dados de conexão
host = prop.get('CON', 'host')
port = prop.getint('CON', 'port')
topic = prop.get('CON', 'topic')
tls = prop.getboolean('CON', 'tls')
# Certificados e chaves para TLS
caPath = prop.get('CERT', 'caPath')
certPath = prop.get('CERT', 'certPath')
keyPath = prop.get('CERT', 'keyPath')
# Dados AWS
clientId = prop.get('CON', 'clientId')
thingName = prop.get('CON', 'thingName')

# Conectando ao broker
if(tls):
    mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
mqttc.connect(host, port, keepalive=300)
mqttc.loop_start()

# Procedimento de envio de mensagens (a cada x segundos definidos no sleep)
while 1==1:
    sleep(2)
    if connflag == True:
        tempreading = uniform(20.1,25.2)
        mqttc.publish(topic, tempreading, qos=0)
        print("Msg sent: %f" % tempreading)
    else:
        print("Waiting for connection...")
