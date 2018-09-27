from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from GoogleGlass.serializers import DocumentSerializer

from GoogleGlass.models import Document
from GoogleGlass.forms import DocumentForm
from rest_framework.parsers import FileUploadParser


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
			serializer.save()
			#print("serializer.data: ",serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


