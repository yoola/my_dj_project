from django import forms

from GoogleGlass.models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('floor', 'room', 'object_type','status','document')

