from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from GoogleGlass.serializers import DocumentSerializer

from GoogleGlass.models import Document
from GoogleGlass.forms import DocumentForm
from rest_framework.parsers import FileUploadParser
from GoogleGlass.Image_recognition.Code.startDetection_upload import main

import base64
import os.path

# HTTPIE: http -f POST http://192.168.178.20:8000/GoogleGlass/documents/ floor='3OG' room='310' document@310try.jpg
# list all Documents or create a new one

class DocumentList(APIView):

	def get(self, request):
		documents = Document.objects.all()
		serializer = DocumentSerializer(documents, many= True, context={'request':request})
		return Response(serializer.data)

	def post(self, request, format=None):
		#print("I'm in POST")
		#print(request.body)
		serializer = DocumentSerializer(data=request.data)

		if serializer.is_valid():
			
			imageName = serializer.validated_data.get('document')
			print("I'm in Post")
			
			dir_ = "/Users/jula/Github/my_dj_project/GoogleGlass/media/documents/"
			imagepath_ = dir_+str(imageName)

			#d = Document.objects.get(document=str("documents/"+str(imageName)))
			#print("d: ",d)
			
			if os.path.isfile(imagepath_):
				print("It is in")
				d = Document.objects.get(document=str("documents/"+str(imageName)))
				new_status = serializer.validated_data.get('status')
				d.status = new_status
				d.save()
				return Response((d.status, 'hi'), status=status.HTTP_201_CREATED)

			else:
				serializer.save()
				print("It is noooot")
				imageType = serializer.validated_data.get('object_type')
			
				imagePath = "/Users/jula/Github/my_dj_project/GoogleGlass/media/documents/"+str(imageName)
				imagePath2 = "/Users/jula/Github/my_dj_project/GoogleGlass/media/documents/310try.jpg"
				context = main(imagePath, str(imageType))
				print(context)

				with open(str(context[0]), "rb") as image_file:
					encoded_string = base64.b64encode(image_file.read())
					#print(encoded_string)
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			#return Response(encoded_string, status=status.HTTP_201_CREATED)
			#return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


