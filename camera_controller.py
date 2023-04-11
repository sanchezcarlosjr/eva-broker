import asyncio
import asyncio_mqtt as aiomqtt
import cv2
import numpy as np

cap = cv2.VideoCapture(4)
resize_width = 320
resize_height = 240
fps = 10
second_per_frame = 1/fps

async def publish_camera_device(client):
  while cap.isOpened():
      success, frame = cap.read()
      frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
      frame = cv2.resize(frame, (resize_width, resize_height))
      retval, buffer = cv2.imencode('.jpg', frame)
      await client.publish("eva/camera/image", payload=buffer.tobytes())
      await asyncio.sleep(second_per_frame)

async def listen():
    async with aiomqtt.Client("158.97.91.177", 8883, username = "eva_cicese", password = "NQz4esJX$") as client:
         await publish_camera_device(client)


asyncio.run(listen())

