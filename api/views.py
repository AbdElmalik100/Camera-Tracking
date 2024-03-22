from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ultralytics import YOLO
from .Tracker import Tracker
import requests
from io import BytesIO
import cv2 as cv
from PIL import Image
import numpy as np



# Create your views here.


class ImageTackingViewSet(ModelViewSet):
    queryset = ImageTacking.objects.all()
    serializer_class = ImageTackingSerializer

    def perform_create(self, serializer):
        result = serializer.save()
        
        tracker_obj = Tracker(video_fbs = 0)
        image_url = serializer.data['image']



        detection = self.perform_object_detection(image_url)


        response = requests.get(image_url)
        image_data = response.content

        img = np.array(Image.open(BytesIO(image_data))) 
        # new_img = cv.resize(src=img, dsize=(760, 700))

        frame = tracker_obj.start_tracking(img, detection, 
                                    draw_canvas=False,
                                    distace_using_speed=False,
                                    distance_using_steps=False, 
                                    detect_faces=True,
                                    draw_distance_line=False)
        
        canvas_object = tracker_obj.person_canvas
        
        for item in canvas_object:
            isntance = DetectionResults.objects.create(
                face = canvas_object[item]['face'].tobytes()
            )
            isntance.save()
            # if "face" in canvas[item] and "canvas" in canvas[item]:    
            #     # tracker_obj.person_canvas[item]['canvas'] = "ha"
            #     # tracker_obj.person_canvas[item]['face'] = "ha"
            #     # canvas[item]['canvas'] = (canvas[item]['canvas']).tobytes()
            #     # canvas[item]['face'] = (canvas[item]['face']).tobytes()
            #     pass

    
    def perform_object_detection(self, image_url):
        # Initialize YOLO model
        model = YOLO("yolov8n.pt")

        # Perform object detection
        results = model.track(image_url, persist = True)
        
        return results[0]




class PositionTrackingViewSet(ModelViewSet):
    queryset = PositionTracking.objects.all()
    serializer_class = PositionTrackingSerializer

class DetectionResultsViewSet(ModelViewSet):
    queryset = DetectionResults.objects.all()
    serializer_class = DetectionResultsSerializer

