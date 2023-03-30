import paho.mqtt.client as mqtt
from matrix_lite import led
import time
from time import sleep
from math import pi, sin


import asyncio

class Proceso:
    def __init__(self):
        self.en_pr = False

    async def procesar(self):
        self.en_proceso = True
        print("toggleOn...")
        await asyncio.sleep(5) # Escuchando al usuario
        self.en_proceso = False
        print("Procesamiento completo.")

    async def esperar_solicitud(proceso):
        while True:
            if not proceso.en_proceso:
                print("Leds encendidas")
            await asyncio.sleep(1)
        else:
            print("Luces apagadas...")
            await asyncio.sleep(1)

proceso = Proceso()

# Creamos el bucle de eventos de asyncio
loop = asyncio.get_event_loop()

# Creamos la tarea para procesar
tarea_proceso = loop.create_task(proceso.procesar())

# Creamos la tarea para esperar por una solicitud
tarea_espera = loop.create_task(esperar_solicitud(proceso))

# Ejecutamos el bucle de eventos de asyncio
loop.run_until_complete(asyncio.gather(tarea_espera, tarea_proceso))


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("hermes/hotword/toggleOn")
    client.subscribe("hermes/asr/stopListening")
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    everloop = ['black'] * led.length
    toggleOn = False

    ledAdjust = 0.0
    if len(everloop) == 35:
        ledAdjust = 0.51 # MATRIX Creator
    else:
        ledAdjust = 1.01 # MATRIX Voice

    frequency = 0.360
    counter = 0.0
    tick = len(everloop) - 1

    while True:
        # Create rainbow
        for i in range(len(everloop)):
            #r = round(max(0, (sin(frequency*counter+(pi/180*240))*155+100)/10))
            #g = round(max(0, (sin(frequency*counter+(pi/180*120))*155+100)/10))
            b = round(max(0, (sin(frequency*counter)*155+100)/10))

            counter += ledAdjust

            everloop[i] = {'b':b}

        led.set(everloop)

        sleep(.035)
        print(msg.topic)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("158.97.91.177", 8883)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()


