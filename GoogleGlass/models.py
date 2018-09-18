from __future__ import unicode_literals
#from GoogleGlass.views import get_image_path
from django.db import models
import os


# def update_filename(instance, filename):
#     path = "documents/"
#     format = instance.description
#     return os.path.join(path, format)

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/') # upload_to=update_filename
    uploaded_at = models.DateTimeField(auto_now_add=True)

