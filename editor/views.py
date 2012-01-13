from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from google.appengine.api import users

def create(request, category):
    user = users.get_current_user()
    if user:
        return direct_to_template(request, "editor/edit.html", { "category" : category, "object_id" : None})
    else:
        return redirect(users.create_login_url(request.get_full_path()))

def update(request, category, objectID):
    user = users.get_current_user()
    if user:
        return direct_to_template(request, "editor/edit.html", { "category" : category, "object_id" : objectID})
    else:
        return redirect(users.create_login_url(request.get_full_path()))
