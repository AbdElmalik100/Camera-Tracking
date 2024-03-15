from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
# from ultralytics import YOLO
# from .Tracker import Tracker

# Create your views here.


class ImageTackingViewSet(ModelViewSet):
    queryset = ImageTacking.objects.all()
    serializer_class = ImageTackingSerializer

    # def perform_create(self, serializer):
    #     result = serializer.save()
    #     tracker_obj = Tracker(video_fbs = 0)
    #     image_url = self.request.build_absolute_uri(result.image.url)
    #     detection = self.perform_object_detection(image_url)
    #     print(detection) # Results
    #     frame = tracker_obj.start_tracking(image_url, detection, 
    #                                 draw_canvas=False,
    #                                 distace_using_speed=False,
    #                                 distance_using_steps=False, 
    #                                 detect_faces=True,
    #                                 draw_distance_line=False)
    #     print(frame)
    
    # def perform_object_detection(self, image_url):
    #     # Initialize YOLO model
    #     model = YOLO("yolov8n.pt")

    #     # Perform object detection
    #     results = model.track(image_url, persist = True)
        
    #     return results[0]








class PositionTrackingViewSet(ModelViewSet):
    queryset = PositionTracking.objects.all()
    serializer_class = PositionTrackingSerializer

