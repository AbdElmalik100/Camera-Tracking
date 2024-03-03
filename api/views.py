from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet

# Create your views here.


class ImageTackingViewSet(ModelViewSet):
    queryset = ImageTacking.objects.all()
    serializer_class = ImageTackingSerializer

class PositionTrackingViewSet(ModelViewSet):
    queryset = PositionTracking.objects.all()
    serializer_class = PositionTrackingSerializer