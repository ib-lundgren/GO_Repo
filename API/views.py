from django.views.generic.simple import direct_to_template
from models import *
from forms import *
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect, QueryDict

# ----------- TMP START?
def showGraphics(request, id=None):
  response = HttpResponse()
  if (id):
    response['Content-Type'] = 'image/png'
    response['Cache-Control'] = 'max-age=7200'
    img = Graphic.get_by_id(int(id))
    if img and img.picture:
      response.content = img.picture
  else:
    for img in Graphic.all():
      response.content += '<a href="/' + img.path + '"><img src="/' + img.path + '"/></a><br/>'  
  return response

def addEnvironment(request):
    return showForm(request, EnvironmentForm(), "Environment")
    
def addVisualGameObject(request):
    return showForm(request, VisualGameObjectForm(), "VisualGameObject")

def addGraphicsObject(request):
    return showForm(request, GraphicForm(), "Graphic")
    
def addGameObject(request):
    form = GameObjectForm()
    return showForm(request, GameObjectForm(), "GameObject")

def showForm(request, form, target):
    return direct_to_template(request, 'api/form.html', {"form":form, "target": "/api/" + target + "/"}) 
# ----------- TMP STOP

# Check type of request and delegate
def handle_objects(request, category=None, **kwargs):
    # Bit of an ugly hack to remove plural (s) to get classname
    if category.lower().endswith('s'):
        category = category[:-1]

    objCls = getattr_nocase("models", category)
    if not objCls:
      return invalid_category(request, category)

    formName = category + "Form"
    formCls = getattr_nocase("forms", formName)
    if not formCls:
      return invalid_category(request, formName)    

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
    if category:
        category = category.capitalize()

    # Bit of an ugly hack to remove plural (s) to get classname
    if category.lower().endswith('s'):
        category = category[:-1]

    objCls = getattr_nocase("models", category)
    if not objCls:
      return invalid_category(request, category)

    formName = category + "Form"
    formCls = getattr_nocase("forms", formName)
    if not formCls:
      return invalid_category(request, formName)
    
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

def getattr_nocase(module, name):
  varList = __import__(module, globals(), locals(), [], -1)
  className = get_class_name_nocase(name, varList)
  if className:
    return getattr(varList, className)

def get_class_name_nocase(name, classStr):
  for c in dir(classStr):
    if name.lower() == c.lower():
      return c

# Tell the user he is trying to access something that aint there =)
def not_implemented(request, objCls, obj=None, formCls=None, **kwargs):
    info = { "status" : "error",
             "message" : "unsupported operation" 
           }
    return json_response(request, info, 404)

# Parse a POST request into an object and save it
def create_new_object(request, objCls, formCls, **kwargs):
    data = request.POST.copy()
    data.update(request.FILES)
    form = formCls(data)
    
    obj = objCls()
    try:
        if form.validate():
            form.populate_obj(obj)
            obj.put()
            return json_response(request, obj.to_dict(), 201)
        else:
            return form_error(request, form, obj) 
    except AttributeError as e:
        raise
        info = { "status" : "error",
                 "message" : e.args}
        return json_response(request, info, 400)

# Create a json error response from a form
def form_error(request, form, obj):
    info = { "status" : "error",
             "message" : form.errors }
    return json_response(request, info, 400)

# Parse a PUT request and update an existing object
def update_object(request, objCls, obj, formCls, **kwargs):
    data = request.POST.copy()
    data.update(request.FILES)
    form = formCls(data)
    
    try:
        if form.validate():
            form.populate_obj(obj)
            obj.put()
            return HttpResponseRedirect("/api/" + objCls.__name__)
        else:
            return form_error(request, form, obj) 
    except AttributeError as e:
        info = { "status" : "error",
                 "message" : e.args}
        return json_response(request, info, 400)

# Get all objects in a category
def get_objects(request, objCls, formCls, **kwargs):
    items = [o.to_dict() for o in objCls.all()]
    return json_response(request, items, 200)    
 
# Get a specific object from category and ID
def get_object(request, objCls, obj, formCls, **kwargs):
    return json_response(request, obj.to_dict(), 200)

# Invalid category
def invalid_category(request, category):
    info = { "status" : "error", 
             "message" : "Invalid category %s" % category}
    return json_response(request, info, 404)

# Invalid object
def invalid_object(request, category, obj):
    info = { "status" : "error",
             "message" : "Invalid object from category %s" % category}
    return json_response(request, info), 404

# Delete an object from a category and ID
def delete_object(request, objCls, obj, formCls, **kwargs):
    try:
        obj.delete()
    except NotSavedError:
        info = { "status" : "error",
                 "message" : "object not saved" }
        return json_response(request, info, 404)

    info = { "status" : "ok",
             "message" : "object deleted" }
    return json_response(request, info, 200)

# Return a json HttpResponse from dict
def json_response(request, info, status=200, **kwargs):
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
    return HttpResponse(json, mimetype="application/json", status=status)    
