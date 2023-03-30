import asyncio
from jsonschema import validate
import asyncio_mqtt as aiomqtt
import json
from pyax12.connection import Connection

servomotor = Connection(port="/dev/ttyUSB0", baudrate=57600)

async def listen(queue):
    async with aiomqtt.Client("158.97.91.177",8883) as client:
        async with client.messages() as messages:
            for key in ['eva/head/animation', "eva/head/settings"]:
                await client.subscribe(key)
            async for message in messages:
                if message.topic.matches("eva/head/settings"):
                   await client.publish("eva/head/settings", payload=0)
                if message.topic.matches("eva/head/animation"):
                   await queue.put((message.topic.value, message.payload.decode("utf-8")))

schema = {
  "type": "object",
  "properties": {
    "onInit": {
      "type": "object"
    },
    "onExec": {
      "type": "object",
      "properties": {
        "unlimited": {
          "type": "boolean"
        },
        "frames": {
          "type": "array",
          "items": {}
        }
      },
      "required": [
        "unlimited",
        "frames"
      ]
    },
    "onDestroy": {
      "type": "object"
    }
  },
  "required": [
    "onInit",
    "onExec",
    "onDestroy"
  ]
}

def onInit(payload):
  pass

def onExec(payload, frame=0):
   unlimited = 'unlimited' in payload and payload['unlimited']
   while unlimited or frame < len(payload['frames']):
     frame = payload['frames'][frame%len(payload['frames'])]
     servomotor.goto(frame['dynamixel_id'], frame['grades'], speed=frame['speed'], degrees=frame['degrees'])
     yield frame['time']
   yield -1

def onDestroy(payload):
  pass

async def start_service(queue):
     while True:
        topic, payload = await queue.get()
        payload = json.loads(str(payload))
        try:
            validate(instance=payload, schema=schema)
            onInit(payload['onInit'])
            frame = 0
            time = 0
            while queue.empty():
               time = next(onExec(payload['onExec'], frame))
               if time < 0:
                   break
               await asyncio.sleep(time)
               frame += 1
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
