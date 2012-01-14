from django.views.generic.simple import direct_to_template
from models import *
from forms import *
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect, QueryDict

# Decorator to check for API keys
def require_key(target):

    def wrapper(request, *args, **kwargs):
        key = request.GET.get("api_key")
        if not key:
            key = request.POST.get("api_key")

        from google.appengine.api import users
        user = users.get_current_user()

        if not key and not user:
            info = { "status" : "error", 
                     "message" : "Not authorized due to missing API key" }
            return json_response(request, info, 403)

        domain = request.META["REMOTE_ADDR"]
       
        usr = None
        for u in RepoUser.all().filter("api_key =", key).filter("domain =", domain):
            usr = u

        if not usr and not user:
            info = { "status" : "error",
                     "message" : "Not authorized, invalid domain %s for API key" % domain}
            return json_response(request, info, 403)

        # Valid user, execute function 
        return target(request, *args, **kwargs)
    return wrapper

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

    views = {   "POST" : handle_update,
                "GET" : get_object,
                "PUT" : not_implemented,
                "DELETE" : delete_object,
                "HEAD" : not_implemented,
                "PATCH" : not_implemented,
        }
    return views.get(request.method)(request, objCls, obj, formCls=formCls, **kwargs)

# We use this because django does not accept data sent with
# a post so any updating of objects has to be awkward :S
def handle_update(request, objCls, obj, formCls, **kwargs):
    obj_id = request.POST.get("obj_id")
    if obj_id:
        return update_object(request, objCls, obj, formCls, **kwargs)
    else:
        return add_to_list(request, objCls, obj, formCls, **kwargs)

def getattr_nocase(module, name):
  varList = __import__(module, globals(), locals(), [], -1)
  className = get_class_name_nocase(name, varList)
  if className:
    return getattr(varList, className)
  else:
    return None

def get_class_name_nocase(name, classStr):
  for c in dir(classStr):
    if name.lower() == c.lower():
      return c
  return None

# Tell the user he is trying to access something that aint there =)
def not_implemented(request, objCls, obj=None, formCls=None, **kwargs):
    info = { "status" : "error",
             "message" : "unsupported operation" 
           }
    return json_response(request, info, 404)

# Parse a POST request into an object and save it
@require_key
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
        info = { "status" : "error",
                 "message" : e.args}
        return json_response(request, info, 400)

# Create a json error response from a form
def form_error(request, form, obj):
    info = { "status" : "error",
             "message" : form.errors,
             "object" : obj.to_dict() }
    return json_response(request, info, 400)

# Parse a PUT request and update an existing object
@require_key
def update_object(request, objCls, obj, formCls, **kwargs):
    data = request.POST.copy()
    data.update(request.FILES)
    form = formCls(data)
    
    try:
        if form.validate():
            form.populate_obj(obj)
            obj.put()
            return json_response(request, obj.to_dict(), 200)
        else:
            return form_error(request, form, obj) 
    except AttributeError as e:
        info = { "status" : "error",
                 "message" : e.args,
                 "error" : e }
        return json_response(request, info, 400)

# Get all objects in a category
def get_objects(request, objCls, formCls, **kwargs):
    items = [o.to_dict() for o in objCls.all()]
    return json_response(request, items, 200)    
 

# Add an object reference to a list of references in this object
# POST request specific, no forms needed
@require_key
def add_to_list(request, objCls, obj, formCls, **kwargs):
    target = request.POST.get("list", None)
    obj_keys = request.POST.get("keys", None)
    obj_cat = request.POST.get("cat", None)

    for prop in objCls.properties():
        if prop == target:
            goCls = getattr_nocase("models", obj_cat)              

            # Check if the category matches an object class
            if not goCls:
                context = { "status" : "error",
                            "message" : "invalid object type in cat, type was %s" % goCat}
                return json_response(request, context, 400)

            # Get objects from the database, skip empty values
            try:
                objs = goCls.get([obj_key for obj_key in obj_keys.split(",") if obj_key])
            except KindError as e:
                context = { "status" : "error", 
                            "message" : "invalid key found, trace was %s" % e}
                return json_response(request, context, 400)

            # Add the objects to our list property
            getattr(obj, prop).extend([o.key() for o in objs if o]) 
            obj.put()

            # Return a representation of the updated object
            return json_response(request, obj.to_dict(), 200)
           
    # Invalid property
    context = { "status" : "error",
                "message" : "invalid property %s" % target} 
    return json_response(request, context, 400)
        

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
# TODO: require_owner
@require_key
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

###### Create new api_key section ######

# Create new api_key
def create_api_key(request):
    domain = request.META["REMOTE_ADDR"]
    from setup import allowed_api_key_creators as allowed
    if not domain in allowed:
        info = { "status" : "error",
                 "message" : "Not authorized" }
        return json_response(request, info, 403)

    # note that we do not validate these! (future work: validate)
    email = request.POST.get("email")
    domain = request.POST.get("domain")
  
    if not email or not domain:
        info = { "status" : "error",
                 "message" : "missing parameter email or domain" }
        return json_response(request, info, 400)

    # the api_key is simple a 20 char long encrypted mix of 
    # user info + secret
    import md5
    api_key = md5.new(email + domain).hexdigest()

    # create and store the new user
    usr = RepoUser(email=email, api_key=api_key, domain=domain)
    usr.put()

    info = { "status" : "ok",
             "message" : "API key successfully created",
             "api_key" : api_key }
    return json_response(request, info, 201)


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
# ----------- TMP STOP
