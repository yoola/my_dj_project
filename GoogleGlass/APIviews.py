from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from GoogleGlass.serializers import DocumentSerializer

from GoogleGlass.models import Document
from GoogleGlass.models import Object

from GoogleGlass.forms import DocumentForm
from rest_framework.parsers import FileUploadParser
from GoogleGlass.Image_recognition.Code.startDetection_upload import main
from rest_framework.renderers import JSONRenderer

import base64
import os.path
import os
import shutil
import glob

dir_source = r"/Users/jula/Github/my_dj_project/GoogleGlass/media/documents/"
dir_database = r"/Users/jula/Github/my_dj_project/GoogleGlass/Image_recognition/Test_Pics_B11/"

# HTTPIE: http -f POST http://192.168.178.20:8000/GoogleGlass/documents/ floor='3OG' room='310' document@310try.jpg
# list all Documents or create a new one
def getID(objectID):
	return((objectID.split("("))[1].split(")")[0])

class DocumentList(APIView):

	def get(self, request):
		documents = Document.objects.all()
		serializer = DocumentSerializer(documents, many= True, context={'request':request})
		return Response(serializer.data)

	def post(self, request, format=None):
		print("I'm in POST")
		print("Request body: ",request.body)
		#requ_body = str(request.body)
		#requ_body = requ_body.replace("\"", "'")
		#print("Requ body: ",requ_body)
		print("Request data: ",request.data)
		serializer = DocumentSerializer(data=request.data)

		if serializer.is_valid():

			serializer.save()		
			toDo = serializer.validated_data.get('todo')

			# send back matches image with status
			if toDo == 'getstatus':	
				# get last image saved
				doc = Document.objects.latest('document')
				obj = Object.objects.get(object_id=doc.object_id)
				
				return Response(obj.status, status=status.HTTP_201_CREATED)
			# http -f POST http://192.168.178.38:8000/GoogleGlass/documents/ todo='editstatus' edit_status_to='FUNNY' object_id='0_h_1OG_Flur192'
			if toDo == 'editstatus':	
				editStatusTo = serializer.validated_data.get('edit_status_to')
				objID = serializer.validated_data.get('object_id')
				obj = Object.objects.get(object_id=objID)
				obj.status = editStatusTo
				obj.save()
				return Response((editStatusTo, objID), status=status.HTTP_201_CREATED)
			# http -f POST http://192.168.178.38:8000/GoogleGlass/documents/ todo='addimage' object_id='0_h_1OG_Flur192'
			elif toDo == 'addimage':
				objID = serializer.validated_data.get('object_id')
				obj = Object.objects.get(object_id=objID)
				newName = "0_4"+objID[1:]+".jpg"
				print(newName)
				# save document in sqlite3 database
				doc = Document(id=None, document =newName, object_id=objID)
				doc.save()
				localPath =dir_database+ str(obj.floor)+"_"+str(obj.room)+"/Object/"#+newName
				for infile in glob.glob( os.path.join(dir_source, '*.jpg') ):
					shutil.move(infile,localPath)
				cut = infile.rfind("/")
				oldName = infile[cut+1:]
				# save document in local database
				print(localPath+str(oldName))
				os.rename(localPath+str(oldName), localPath+newName)

				for infile in glob.glob( os.path.join(dir_source, '*.jpg') ):
					os.remove(infile)

				doc_old1 = Document.objects.filter(document="documents/"+oldName)
				doc_old2 = Document.objects.filter(document="documents/None/No_images.jpg/")
				doc_old1.delete()
				doc_old2.delete()
				return Response(("Add image with object id: "+ objID), status=status.HTTP_201_CREATED)
			# http -f POST http://192.168.178.38:8000/GoogleGlass/documents/ todo='deleteimage' object_id='0_h_1OG_Flur192'
			elif toDo == 'deleteimage':
				for infile in glob.glob( os.path.join(dir_source, '*.jpg') ):
					oldName = infile
					os.remove(infile)
				cut = infile.rfind("/")
				oldName = oldName[cut+1:]
				doc_old1 = Document.objects.filter(document="documents/"+oldName)
				doc_old2 = Document.objects.filter(document="documents/None/No_images.jpg/")
				doc_old1.delete()
				doc_old2.delete()
					
				return Response(("Deleted image."), status=status.HTTP_201_CREATED)
			# send an existent object_id
			# http -f POST http://192.168.178.20:8000/GoogleGlass/documents/ object_type='h' object_id='0_h_1OG_Flur192' document@192try.jpg todo='process'
			# http -f POST http://192.168.178.38:8000/GoogleGlass/documents/ object_type='h' object_id='0_h_1OG_Flur192' document@192try.jpg todo='process'
			else:
				#
				print("process this image")
				imageName = serializer.validated_data.get('document')
				imagePath = dir_source+str(imageName)
				#objType = serializer.validated_data.get('object_type')
				#print("objType: ", objType)
				context = main(imagePath)
				context = context[0]
				pos = context.rfind("/")
				context_id = context[pos+1:]
				doc = Document.objects.get(document=context_id)

				#objID2 = getID(str(doc.object_id))
				#print("objID:", doc.object_id)
				obj = Object.objects.get(object_id=doc.object_id)
				doc2 = Document(id=None, document ="temp", object_id=doc.object_id)
				doc2.save()

				with open(str(context), "rb") as image_file:
					encoded_string = base64.b64encode(image_file.read())
				#return Response(serializer.data, status=status.HTTP_201_CREATED)
				return Response(encoded_string, status=status.HTTP_201_CREATED)
	
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)