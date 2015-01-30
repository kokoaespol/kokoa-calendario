from django.conf.urls import patterns, include, url
from django.shortcuts import render
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from webapp import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'webapp.views.ingresar'),
	url(r'^admin/', include(admin.site.urls)),
     url(r'^horario/', 'webapp.views.horario')
	
) + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


