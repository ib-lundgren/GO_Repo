from django.views.generic.simple import direct_to_template

def create_environment(request):
    context = { "page_header" : "Create a new Environment Object", }
    return direct_to_template(request, "editor/environment.html", context)