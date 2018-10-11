from django import forms

from GoogleGlass.models import Document

from GoogleGlass.models import Object

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('floor', 'room', 'object_type','status','document')

class Object(forms.ModelForm):
    class Meta:
        model = Object
        fields = ('object_id', 'object_type', 'status')

