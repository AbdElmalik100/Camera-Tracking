from django.db import models

# Create your models here.



class ImageTacking(models.Model):
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    image = models.ImageField(upload_to = 'images', blank=True, null=True)



class PositionTracking(models.Model):
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    position = models.CharField(max_length = 255)