import random
from datetime import datetime
from ultralytics import YOLO
import cv2 as cv
import numpy as np
import time as time
from Tracker import Tracker

VID_WIDTH = 760
VID_HEIGHT = 700
cams = {
    4: cv.VideoCapture("ai-team-2024\Central Park People Watching - 1080.mp4"),
}


# Run once
model = YOLO("models\yolov8n.pt")
tracker_obj = Tracker(video_fbs = 0)

while True:
  for key in cams.keys():
    ret, frame = cams[key].read()
    if not ret:
      break
    frame = cv.resize(frame, (VID_WIDTH, VID_HEIGHT))
    
    # Predict then return the results
    results = model.track(frame, persist = True)    
    frame = tracker_obj.start_tracking(frame, results[0], detect_faces=True)
                                      
                                      
    cv.imshow(f"Cam {key}", frame)
  if cv.waitKey(1) & 0xFF == ord('q'):
    break

for cap in cams.values():
  cap.release()
cv.destroyAllWindows()