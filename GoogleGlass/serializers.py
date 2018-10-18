from rest_framework import serializers # serializers converts models e.g. to json data
from .models import Document
from django.http import HttpResponse

class DocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Document
		# returns only the status when requesting information about the Document
		# variations: fields = ('status', 'room'), field = '__all__' 
		#fields = ('__all__')
		fields = ('object_id','object_type','document','todo','edit_status_to')
