from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register("image-tracking", ImageTackingViewSet)
router.register("position-tracking", PositionTrackingViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]