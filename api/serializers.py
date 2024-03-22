from rest_framework import serializers
from .models import *



class ImageTackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTacking
        fields = '__all__'


class PositionTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionTracking
        fields = '__all__'

class DetectionResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectionResults
        fields = '__all__'