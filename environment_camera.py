import asyncio
import asyncio_mqtt as aiomqtt
import base64
import cv2

cap = cv2.VideoCapture(0)
resize_width = 480
resize_height = 320
fps = 24 # frames per second
frame_interval = 1/fps # second per frame
MQTT_QOS=0

async def publish_video_from_camera(client):
  while cap.isOpened():
      success, frame = cap.read()
      frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGBA)
      frame = cv2.resize(frame, (resize_width, resize_height))
      retval, buffer = cv2.imencode('.jpg', frame)
      if retval:
         await client.publish("environment/camera/lab", payload=base64.b64encode(buffer), qos=MQTT_QOS)
      await asyncio.sleep(frame_interval)

async def listen():
    async with aiomqtt.Client("158.97.91.177", 8883, username="eva_cicese", password="NQz4esJX$") as client:
         await publish_video_from_camera(client)


asyncio.run(listen())
