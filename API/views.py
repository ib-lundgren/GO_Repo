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

# Check type of request and delegate
def handle_objects(request, category=None):
	views = {  "POST" : create_new_object,
		   "GET" : get_objects,
		   "PUT" : not_implemented,
	           "DELETE" : not_implemented,
		   "HEAD" : not_implemented,
		   "PATCH" : not_implemented,
		}
	return views.get(request.method)(request, category)

# Check type of request and delegate
def handle_object(request, category=None, objectID=None):
	views = {  "POST" : not_implemented,
		   "GET" : get_object,
		   "PUT" : update_object,
		   "DELETE" : delete_object,
		   "HEAD" : not_implemented,
		   "PATCH" : not_implemented,
		}
	return views.get(request.method)(request, category, objectID)	

# Tell the user he is trying to access something that aint there =)
def not_implemented(request, **kwargs):
	pass

# Parse a POST request into an object and save it
def create_new_object(request, category=None):
	pass

# Parse a PUT request and update an existing object
def update_object(request, category=None, objectID=None):
	pass

# Get all objects in a category
def get_objects(request, category=None, filter=None):
	pass

# Get a specific object from category and ID
def get_object(request, category=None):
	pass

# Delete an object from a category and ID
def delete_object(request, category=None, objectID=None):
	pass


