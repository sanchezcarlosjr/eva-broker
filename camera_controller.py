import asyncio
import asyncio_mqtt as aiomqtt
import base64
import cv2

cap = cv2.VideoCapture(4)
resize_width = 320
resize_height = 240
fps = 20 # frames per second
frame_interval = 1/fps # second per frame
MQTT_QOS=0

async def publish_video_from_camera(client):
  while cap.isOpened():
      success, frame = cap.read()
      # TODO: Should we change to gray scale?
      frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGBA)
      frame = cv2.resize(frame, (resize_width, resize_height))
      retval, buffer = cv2.imencode('.jpg', frame)
      if retval:
          # TODO: Should we compress with Brotli?
         await client.publish("eva/camera/image", payload=base64.b64encode(buffer), qos=MQTT_QOS)
      await asyncio.sleep(frame_interval)

async def listen():
    async with aiomqtt.Client("localhost", 8883) as client:
         await publish_video_from_camera(client)


asyncio.run(listen())
