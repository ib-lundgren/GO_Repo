from django.views.generic.simple import direct_to_template

def create(request, category):
    return direct_to_template(request, "editor/edit.html", { "category" : category, "object_id" : None})

def update(request, category, objectID):
    return direct_to_template(request, "editor/edit.html", { "category" : category, "object_id" : objectID})
