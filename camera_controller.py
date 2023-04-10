import asyncio
import json
import asyncio_mqtt as aiomqtt
import base64

# https://gist.github.com/khalidmeister/ea292150905d748457d8f6c19ec095c3
import cv2
import numpy as np

cap = cv2.VideoCapture(4)

async def publish_camera_device(client):
  while cap.isOpened():
      success, image = cap.read()

      # Flip the image horizontally for a later selfie-view display
      # Also convert the color space from BGR to RGB
      image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

      # Convert the color space from RGB to BGR
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

      img_h, img_w, img_c = image.shape

      retval, buffer = cv2.imencode('.jpg', image)
      base64_image = base64.b64encode(buffer).decode('utf-8')

      await client.publish("eva/camera/image", payload=base64_image)
      await asyncio.sleep(0.01)

async def listen():
    async with aiomqtt.Client("158.97.91.177", 8883, username = "eva_cicese", password = "NQz4esJX$") as client:
         await publish_camera_device(client)


asyncio.run(listen())

