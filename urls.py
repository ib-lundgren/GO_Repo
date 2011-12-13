from django.conf.urls.defaults import patterns, include, url
from info.views import index, plan, repo, doc, contact
from progress.views import progress
from API.views import *
from editor.views import *
from browser.views import *

urlpatterns = patterns('',
    (r'^$', index),
    (r'api/add/Graphics', addGraphicsObject),
    (r'api/add/Environment', addEnvironment),
    (r'api/add/GameObject', addGameObject),
    (r'api/add/VisualGameObject', addVisualGameObject),
    (r'api/image[s]*/(\d+)?', showGraphics),
    (r'^create/Environment/$', create_environment),
    (r'^create/(?P<category>\w+)/(?P<objectID>\d+)/$', update),
    (r'^create/(?P<category>\w+)/$', create),
    (r'^browse/(?P<category>\w+)/$', browse),
    (r'^api/(?P<category>\w+)/(?P<objectID>\d+)/$', handle_object),
    (r'^api/(?P<category>\w+)/(?P<filter>\w+)/$', handle_objects),
    (r'^api/(?P<category>\w+)/$', handle_objects),
    (r'plan', plan),
    (r'progress', progress), 
    (r'doc', doc), 
    (r'contact', contact),      
    (r'repository', repo),
)
