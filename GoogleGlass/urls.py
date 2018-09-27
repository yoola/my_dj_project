from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from GoogleGlass.models import Document

from . import views
from . import APIviews

urlpatterns = [
	url(r'^$', views.home, name='home'),
    url(r'^form/$', views.model_form_upload, name='model_form_upload'),
    url(r'^results/$', views.image_results, name='image_results'),
    url(r'^documents/$', APIviews.DocumentList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
