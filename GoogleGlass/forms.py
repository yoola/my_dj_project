from django import forms

from GoogleGlass.models import Document
from GoogleGlass.models import Object

class Object(forms.ModelForm):
    class Meta:
        model = Object
        fields = ('object_id', 'object_type', 'floor','room','status',)

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('object_id','object_type','document','todo','edit_status_to',)