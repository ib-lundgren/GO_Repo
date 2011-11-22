from django.conf.urls.defaults import patterns, include, url
from info.views import index, plan, repo, doc, contact
from progress.views import progress

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', index),
    (r'plan', plan),
    (r'progress', progress), 
    (r'doc', doc), 
    (r'contact', contact),      
    (r'repository', repo),
)
