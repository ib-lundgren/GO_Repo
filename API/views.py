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
	m = __import__("models", globals(), locals(), [], -1)
	if not hasattr(m, category):
		return invalid_category(request, category)
	
	formName = category + "Form"
	f = __import__("forms", globals(), locals(), [], -1)
	if not hasattr(f, formName):
		return invalid_category(request, category)

	formCls = getattr(f, formName)
	
	objCls = getattr(m, category)

	views = {  "POST" : create_new_object,
		   "GET" : get_objects,
		   "PUT" : not_implemented,
	           "DELETE" : not_implemented,
		   "HEAD" : not_implemented,
		   "PATCH" : not_implemented,
		}
	return views.get(request.method)(request, objCls, formCls=formCls)

# Check type of request and delegate
def handle_object(request, category=None, objectID=None):
	m = __import__("models", globals(), locals(), [], -1)
	if not hasattr(m, category):
		return invalid_category(request, category)
	objCls = getattr(m, category)
	
	formName = category + "Form"
	f = __import__("forms", globals(), locals(), [], -1)
	if not hasattr(f, formName):
		return invalid_category(request, category)

	formCls = getattr(f, formName)
	
	obj = objCls.get_by_id(objectID)
	if not obj:
		return invalid_object(request, category, objectID)

	views = {  "POST" : not_implemented,
		   "GET" : get_object,
		   "PUT" : update_object,
		   "DELETE" : delete_object,
		   "HEAD" : not_implemented,
		   "PATCH" : not_implemented,
		}
	return views.get(request.method)(request, objCls, obj, formCls=formCls)	
# Tell the user he is trying to access something that aint there =)
def not_implemented(request, **kwargs):
	pass

# Parse a POST request into an object and save it
def create_new_object(request, objCls, formCls):
	form = formCls(request.POST)
	obj = objCls()
	if form.validate():
		form.populate_obj(obj)
		obj.put()
		return HttpResponseRedirect("api/" + category)
	else:
		return form_error(request, form, obj) 

# Create a json error response from a form
def form_error(request, form, obj):
	info = { 'obj' : obj,
		 'form' : form,
		 'errors' : form.errors,
		}
	return direct_to_template(request, "api/error.html", {'info':info})

# Parse a PUT request and update an existing object
def update_object(request, objCls, obj, formCls):
	form = formCls(request.PUT)
	if form.validate():
                form.populate_obj(obj)
                obj.put()
                return HttpResponseRedirect("api/" + category)
        else:
                return form_error(request, form, obj)
	

# Get all objects in a category
def get_objects(request, objCls, formCls):
	items = simplejson.dumps([o.to_dict() for o in objCls.all()], indent=3)
	return direct_to_template(request, "api/list.html", {"items":items})
 
# Get a specific object from category and ID
def get_object(request, objCls, obj, formCls):
	item = simplejson.dumps(obj.to_dict())
	return direct_to_template(request, "api/single.html", {"item":item}) 

# Invalid category
def invalid_category(request, category):
	info = { "category" : category }
	return direct_to_template(request, "api/invalid_category.html", info)

# Invalid object
def invalid_object(request, category, obj):
	info = { "obj" : obj }
	return direct_to_template(request, "api/invalid_object.html", info)

# Delete an object from a category and ID
def delete_object(request, category=None, objectID=None):
 	# like get obj but delete and return confirm json
	info = { "msg" : "object X deleted" }
	return direct_to_tempate(request, "api/confirm.html", info)

