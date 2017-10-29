'''
This source is part of:
https://www.hackster.io/mariocannistra/radio-astronomy-with-rtl-sdr-raspberrypi-and-amazon-aws-iot-45b617

Use this program to test the AWS IoT certificates received by the author
to participate to the spectrogram sharing initiative on AWS cloud

This program will subscribe and show all the messages sent by its companion
awsiotpub.py using the AWS IoT hub
'''

# Importações
import paho.mqtt.client as paho
import os
import socket
import ssl
import configparser
from struct import *

# Definição de funções
# Ao conectar
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc) )
    client.subscribe(topic, 1 )
    # Ao se inscrever no tópico dentro da função on_connect(), a inscrição é
    # automaticamente renovada quando se reconecta ao broker

# Ao receber mensagem
def on_message(client, userdata, msg):    
    print(msg.payload.decode())

# Ao se inscrever em um tópico (dispensável)
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

# Chamadas de função
mqttc = paho.Client()
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message
mqttc.on_connect = on_connect

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
mqttc.connect(host, port, keepalive=60)
mqttc.loop_forever()
