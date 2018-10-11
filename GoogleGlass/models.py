from __future__ import unicode_literals
#from GoogleGlass.views import get_image_path
from django.db import models
import os


# def update_filename(instance, filename):
#     path = "documents/"
#     format = instance.description
#     return os.path.join(path, format)

class Document(models.Model):
	floor = models.CharField(max_length=10, blank=True)
	room = models.CharField(max_length=10, blank=True)
	object_type = models.CharField(max_length=2, blank=True)
	status = models.CharField(max_length=10, blank=True)
	document = models.ImageField(upload_to='documents/', default='documents/None/No_images.jpg/')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	#document = models.FileField(upload_to='documents/') # upload_to=update_filename
	
class Object(models.Model):
	object_id = models.CharField(max_length=10, blank=True)
	object_type = models.CharField(max_length=10, blank=True)
	status = models.CharField(max_length=10, blank=True)