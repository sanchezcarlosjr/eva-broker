import asyncio
import asyncio_mqtt as aiomqtt

# https://gist.github.com/khalidmeister/ea292150905d748457d8f6c19ec095c3
import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(2)

async def publish_camera_device(client):
  while cap.isOpened():
      success, image = cap.read()

      # Flip the image horizontally for a later selfie-view display
      # Also convert the color space from BGR to RGB
      image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

      # To improve performance
      image.flags.writeable = False

      # Get the result
      results = face_mesh.process(image)

      # To improve performance
      image.flags.writeable = True

      # Convert the color space from RGB to BGR
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

      img_h, img_w, img_c = image.shape
      face_3d = []
      face_2d = []

      if results.multi_face_landmarks:
          for face_landmarks in results.multi_face_landmarks:
              for idx, lm in enumerate(face_landmarks.landmark):
                  if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                      if idx == 1:
                          nose_2d = (lm.x * img_w, lm.y * img_h)
                          nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 8000)

                      x, y = int(lm.x * img_w), int(lm.y * img_h)

                      # Get the 2D Coordinates
                      face_2d.append([x, y])

                      # Get the 3D Coordinates
                      face_3d.append([x, y, lm.z])

              # Convert it to the NumPy array
              face_2d = np.array(face_2d, dtype=np.float64)

              # Convert it to the NumPy array
              face_3d = np.array(face_3d, dtype=np.float64)

              # The camera matrix
              focal_length = 1 * img_w

              cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                      [0, focal_length, img_w / 2],
                                      [0, 0, 1]])

              # The Distance Matrix
              dist_matrix = np.zeros((4, 1), dtype=np.float64)

              # Solve PnP
              success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

              # Get rotational matrix
              rmat, jac = cv2.Rodrigues(rot_vec)

              # Get angles
              angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

              # Get the rotation degrees
              x = angles[0] * 360
              y = angles[1] * 360

              # See where the user's head tilting
              payload = "L" if y < -10 else "R" if y > 10 else "D" if x < -10 else "F"
              await client.publish("eva/camera/headtilting", payload=payload)
              await asyncio.sleep(12)

async def listen():
    async with aiomqtt.Client("158.97.91.177", 8883) as client:
         await publish_camera_device(client)


asyncio.run(listen())

