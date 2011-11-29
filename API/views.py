from django.views.generic.simple import direct_to_template
from forms import *
from models import *
from django.utils import simplejson
from django.http import HttpResponseRedirect

def test(request):
	go = GameObjectForm()
	return direct_to_template(request, 'api/form.html', {"form":go}) 

def objects(request):
	if request.method == 'GET':
            items = simplejson.dumps([o.to_dict() for o in GameObject.all()], indent=3)
	    return direct_to_template(request, 'api/list.html', { "items":items})
	elif request.method == 'POST':
	    item = GameObjectForm(data=request.POST)
	    if item.is_valid():
		item.save()
		return HttpResponseRedirect('/api/objects')
	    else:
		items = simplejson.dumps(dict("error", "invalid input"))
		return direct_to_template(request, 'api/list.html', {"items":items})
