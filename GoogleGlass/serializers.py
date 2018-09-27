from rest_framework import serializers # serializers converts models e.g. to json data
from .models import Document
from drf_extra_fields.fields import Base64ImageField
from GoogleGlass.Image_recognition.Code.startDetection_upload import main

class DocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Document
		# returns only the status when requesting information about the Document
		# variations: fields = ('status', 'room'), field = '__all__' 
		#fields = ('__all__')
		fields = ('floor', 'room', 'object_type','status','document',)

	def create(self, validated_data):
		floor_ = validated_data.get('floor')
		image_ = validated_data.get('document')
		val_dat = Document.objects.create(**validated_data)# return val_dat
		context = main("/Users/jula/Github/my_dj_project/GoogleGlass/media/documents/"+str(image_), 'h')
		print("val_dat: ",val_dat.document)
		return val_dat