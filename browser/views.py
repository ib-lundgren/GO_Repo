from django.views.generic.simple import direct_to_template

def browse(request, category):
    context = { "category" : category }
    return direct_to_template(request, "browser/browse.html", context)
