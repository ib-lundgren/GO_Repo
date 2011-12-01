from django.conf.urls.defaults import patterns, include, url
from info.views import index, plan, repo, doc, contact
from progress.views import progress
from API.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', index),
    (r'api/objects', objects),
    (r'api/add/graphics', addGraphicsObject),
    (r'api/add/environment', addEnvironment),
    (r'api/add/gameObject', addGameObject),
    (r'api/images/(\d+)?', showGraphics),
    (r'^api/(?P<category>\w+)/$', handle_objects),
    (r'^api/(?P<category>\w+)/(?P<filter>\w+)/$', get_objects),
    (r'^api/(?P<category>\w+)/(?P<objectID>\d+)/$', handle_object),
    (r'plan', plan),
    (r'progress', progress), 
    (r'doc', doc), 
    (r'contact', contact),      
    (r'repository', repo),
)
