from django.contrib import admin

from .models import Document
from .models import Object

admin.site.register(Object)
admin.site.register(Document)

