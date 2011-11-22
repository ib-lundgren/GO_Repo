from django.views.generic.simple import direct_to_template

def plan(request):
   return direct_to_template(request, 'info/plan.html', {})
   
def repo(request):
   return direct_to_template(request, 'info/repository.html', {})

def contact(request):
   return direct_to_template(request, 'info/contact.html', {})

def doc(request):
   return direct_to_template(request, 'info/doc.html', {})

def index(request):
   return direct_to_template(request, 'info/index.html', {})
