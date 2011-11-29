from google.appengine.ext.db import djangoforms
from models import *

class GameObjectForm(djangoforms.ModelForm):
	class Meta:
		model = GameObject
