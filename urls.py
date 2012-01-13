from django.conf.urls.defaults import patterns, include, url
from info.views import index, plan, repo, doc, contact, tutorial
from progress.views import progress
from API.views import *
from editor.views import *
from browser.views import *

urlpatterns = patterns('',
    (r'^$', index),
    (r'api/image[s]*/(\d+)?', showGraphics),
    (r'^create/(?P<category>\w+)/(?P<objectID>\d+)/$', update),
    (r'^create/(?P<category>\w+)/$', create),
    (r'^browse/(?P<category>\w+)/$', browse),
    (r'^api/key/', create_api_key),
    (r'^api/(?P<category>\w+)/(?P<objectID>\d+)/$', handle_object),
    (r'^api/(?P<category>\w+)/(?P<filter>\w+)/$', handle_objects),
    (r'^api/(?P<category>\w+)/$', handle_objects),
    (r'plan', plan),
    (r'progress', progress), 
    (r'doc', doc), 
    (r'tutorial', tutorial), 
    (r'contact', contact),      
    (r'repository', repo),
)
