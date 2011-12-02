from django.views.generic.simple import direct_to_template
from models import *
from forms import *
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect

# ----------- TMP START?
def showGraphics(request, id=None):
  response = HttpResponse()
  if (id):
    response['Content-Type'] = 'image/png'
    response['Cache-Control'] = 'max-age=7200'
    img = Graphics.get_by_id(int(id))
    if img and img.picture:
      response.content = img.picture
  else:
    for img in Graphics.all():
      response.content += '<a href="/' + img.path + '"><img src="/' + img.path + '"/></a><br/>'  
  return response

def objects(request):
    if request.method == 'GET':
        items = simplejson.dumps([o.to_dict() for o in GameObject.all()], indent=3)
        # jQuery JSON from external URL apparently requires a callback!
        callback = request.GET.get("callback")
        if (callback):
          items = callback + "(" + items + ")"
        return HttpResponse(items, mimetype='application/json')
    elif request.method == 'POST':
        title = request.POST.get("title")
        description = request.POST.get("description")
        picture = request.FILES.get("picture")
        if title and description:
          g = Graphics()
          g.title = title
          g.description = description
          g.picture = picture.read()
          g.save()
          g.path = "api/image/" + str(g.key().id())
          g.put()
        return HttpResponseRedirect('/api/objects')
    else:
        items = simplejson.dumps(dict("error", "invalid input"))
        return direct_to_template(request, 'api/list.html', {"items":items})

def addEnvironment(request):
    return showForm(request, EnvironmentForm(), "Environment")
    
def addVisualGameObject(request):
    return showForm(request, VisualGameObjectForm(), "VisualGameObject")

def addGraphicsObject(request):
    return showForm(request, GraphicsForm(), "objects")
    
def addGameObject(request):
    form = GameObjectForm()
    return showForm(request, GameObjectForm(), "GameObject")

def showForm(request, form, target):
    return direct_to_template(request, 'api/form.html', {"form":form, "target": "/api/" + target + "/"}) 
# ----------- TMP STOP
    
    
# Check type of request and delegate
def handle_objects(request, category=None, **kwargs):
    m = __import__("models", globals(), locals(), [], -1)
    if not hasattr(m, category):
        return invalid_category(request, category)
    
    formName = category + "Form"
    f = __import__("forms", globals(), locals(), [], -1)
    if not hasattr(f, formName):
        return invalid_category(request, category)

    formCls = getattr(f, formName)
    
    objCls = getattr(m, category)

    views = {   "POST" : create_new_object,
                "GET" : get_objects,
                "PUT" : not_implemented,
                "DELETE" : not_implemented,
                "HEAD" : not_implemented,
                "PATCH" : not_implemented,
        }
    return views.get(request.method)(request, objCls, formCls=formCls, **kwargs)

# Check type of request and delegate
def handle_object(request, category=None, objectID=None, **kwargs):
    m = __import__("models", globals(), locals(), [], -1)
    if not hasattr(m, category):
        return invalid_category(request, category)
    objCls = getattr(m, category)
    
    formName = category + "Form"
    f = __import__("forms", globals(), locals(), [], -1)
    if not hasattr(f, formName):
        return invalid_category(request, category)

    formCls = getattr(f, formName)
    
    try:
        objectID = int(objectID)
    except ValueError:
        return invalid_object(request, category, objectID)
    
    obj = objCls.get_by_id(objectID)
    if not obj:
        return invalid_object(request, category, objectID)

    views = {   "POST" : not_implemented,
                "GET" : get_object,
                "PUT" : update_object,
                "DELETE" : delete_object,
                "HEAD" : not_implemented,
                "PATCH" : not_implemented,
        }
    return views.get(request.method)(request, objCls, obj, formCls=formCls, **kwargs)
    
# Tell the user he is trying to access something that aint there =)
def not_implemented(request, **kwargs):
    info = { "status" : "error",
             "message" : "unsupported operation" 
           }
    return json_response(request, info)

# Parse a POST request into an object and save it
def create_new_object(request, objCls, formCls, **kwargs):
    form = formCls(request.POST)
    obj = objCls()
    if form.validate():
        form.populate_obj(obj)
        obj.put()
        return HttpResponseRedirect("/api/" + objCls.__name__)
    else:
        return form_error(request, form, obj) 

# Create a json error response from a form
def form_error(request, form, obj):
    info = { "status" : "error",
             "messsage" : form.errors }
    return json_response(request, info)

# Parse a PUT request and update an existing object
def update_object(request, category, objCls, obj, formCls, **kwargs):
    form = formCls(request.POST) # Django doesnt use PUT
    if form.validate():
        form.populate_obj(obj)
        obj.put()
        return HttpResponseRedirect("api/" + category)
    else:
        return form_error(request, form, obj)
    

# Get all objects in a category
def get_objects(request, objCls, formCls, **kwargs):
    items = [o.to_dict() for o in objCls.all()]
    return json_response(request, items)    
 
# Get a specific object from category and ID
def get_object(request, objCls, obj, formCls, **kwargs):
    return json_response(request, obj.to_dict())

# Invalid category
def invalid_category(request, category):
    info = { "status" : "error", 
             "message" : "Invalid category %s" % category}
    return json_response(request, info)

# Invalid object
def invalid_object(request, category, obj):
    info = { "status" : "error",
             "message" : "Invalid object from category %s" % category}
    return json_response(request, info)

# Delete an object from a category and ID
def delete_object(request, objCls, obj, formCls, **kwargs):
    try:
        obj.delete()
    except NotSavedError:
        info = { "status" : "error",
                 "message" : "object not saved" }
        return json_response(request, info)

    info = { "status" : "ok",
             "message" : "object deleted" }
    return json_response(request, info)

# Return a json HttpResponse from dict
def json_response(request, info, **kwargs):
    json = simplejson.dumps(info, indent=3)
    # For some reason Django puts all raw data in POST instead
    # of where it "should be" imo
    methods = { "GET" : request.GET,
                "POST" : request.POST,
                "PUT" : request.POST,
                "DELETE" : request.POST,
                "HEAD" : request.POST,
                "PATCH" : request.POST,
              }
    callback = methods.get(request.method).get("callback")
    if callback:
        json = callback + "(" + json + ")"
    return HttpResponse(json, mimetype="application/json")    
