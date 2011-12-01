from django.views.generic.simple import direct_to_template
from models import *
from forms import *
from django.utils import simplejson
from django.http import HttpResponseRedirect

def showForm(request, form):
    return direct_to_template(request, 'api/form.html', {"form":form}) 
    
def addEnvironment(request):
    return showForm(request, EnvironmentForm())
    
def addVisualGameObject(request):
    return showForm(request, VisualGameObjectForm())
    
def test(request):
    form = GameObjectForm()
    return direct_to_template(request, 'api/form.html', {"form":form}) 

def objects(request):
	if request.method == 'GET':
            items = simplejson.dumps([o.to_dict() for o in GameObject.all()], indent=3)
	    return direct_to_template(request, 'api/list.html', { "items":items})
	elif request.method == 'POST':
	    title = request.POST.get("title")
	    description = request.POST.get("description")
	    if title and description:
		go = GameObject()
		go.title = title
		go.description = description
		go.put()
		return HttpResponseRedirect('/api/objects')
	    else:
		items = simplejson.dumps(dict("error", "invalid input"))
		return direct_to_template(request, 'api/list.html', {"items":items})
