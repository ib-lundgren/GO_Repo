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
    (r'api/add/visualObject', addVisualGameObject),
    (r'api/add/environment', addEnvironment),
    (r'api/example', test),
    (r'^api/(?P<category>\w+)/$', handle_objects),
    (r'^api/(?P<category>\w+)/(?P<filter>\w+)/$', get_objects),
    (r'^api/(?P<category>\w+)/(?P<objectID>\d+)/$', handle_object),
    (r'plan', plan),
    (r'progress', progress), 
    (r'doc', doc), 
    (r'contact', contact),      
    (r'repository', repo),
)
