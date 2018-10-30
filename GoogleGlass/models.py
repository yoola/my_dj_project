from __future__ import unicode_literals
#from GoogleGlass.views import get_image_path
from django.db import models
import os


# def update_filename(instance, filename):
#     path = "documents/"
#     format = instance.description
#     return os.path.join(path, format)

	
class Object(models.Model):
	object_id = models.CharField(max_length=20, primary_key=True)
	object_type = models.CharField(max_length=10, blank=True)
	floor = models.CharField(max_length=10, blank=True)
	room = models.CharField(max_length=10, blank=True)
	status = models.CharField(max_length=10, blank=True)


class Document(models.Model):
	object_id = models.CharField(max_length=20, blank=True)
	#object_id = models.ForeignKey(Object, default='DEFAULT VALUE', on_delete=models.CASCADE)
	object_type = models.CharField(max_length=10, blank=True)
	document = models.ImageField(upload_to='documents/', default='documents/None/No_images.jpg/')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	todo = models.CharField(max_length=20, blank=True)
	edit_status_to = models.CharField(max_length=10, blank=True)
	#document = models.FileField(upload_to='documents/') # upload_to=update_filename

# python3 manage.py shell
# obj1 = Object(object_id = '2_f_2OG_Flur295',object_type='f',floor='2', room='295',status='OK')
# obj1.save()
# doc1 = Document(id= None, document='2_2_f_2OG_Flur295.jpg',object_id=obj1)
# doc1.save()
