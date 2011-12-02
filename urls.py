from django.conf.urls.defaults import patterns, include, url
from info.views import index, plan, repo, doc, contact
from progress.views import progress
from API.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', index),
    (r'api/add/Graphics', addGraphicsObject),
    (r'api/add/Environment', addEnvironment),
    (r'api/add/GameObject', addGameObject),
    (r'api/add/VisualGameObject', addVisualGameObject),
    (r'api/image[s]*/(\d+)?', showGraphics),
    (r'^api/(?P<category>\w+)/(?P<objectID>\d+)/$', handle_object),
    (r'^api/(?P<category>\w+)/(?P<filter>\w+)/$', handle_objects),
    (r'^api/(?P<category>\w+)/$', handle_objects),
    (r'plan', plan),
    (r'progress', progress), 
    (r'doc', doc), 
    (r'contact', contact),      
    (r'repository', repo),
)
