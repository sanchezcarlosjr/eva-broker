import asyncio
from jsonschema import validate
import paho.mqtt as mqtt
import asyncio_mqtt as aiomqtt
import json
from matrix_lite import led

async def listen(queue):
    async with aiomqtt.Client("158.97.91.177", 8883, username = "eva_cicese", password = "NQz4esJX$") as client:
        async with client.messages() as messages:
            for key in ['eva/matrixvoice/leds/animation', "eva/matrixvoice/leds/settings"]:
                await client.subscribe(key)
            async for message in messages:
                if message.topic.matches("eva/matrixvoice/leds/settings"):
                   await client.publish("eva/matrixvoice/leds/response_settings", payload=led.length)
                if message.topic.matches("eva/matrixvoice/leds/animation"):
                   await queue.put((message.topic.value, message.payload.decode("utf-8")))

async def start_service(queue):
     while True:
        topic, payload = await queue.get()
        payload = json.loads(str(payload))
        try:
            validate(instance=payload, schema=schema)
            onInit(payload['onInit'])
            frame = 0
            while queue.empty() and next(onExec(payload['onExec'], frame)):
               frame += 1
               await asyncio.sleep(payload['onExec']['sleep'])
            onDestroy(payload['onDestroy'])
        except Exception as e:
            print(payload,e)

async def main():
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    task = loop.create_task(listen(queue))
    await start_service(queue)
    await task


asyncio.run(main())
