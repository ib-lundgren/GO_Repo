from wtforms.ext.appengine.db import model_form
from models import *

GameObjectForm = model_form(GameObject)
VisualGameObjectForm = model_form(VisualGameObject)
EnvironmentForm = model_form(Environment)
GraphicsForm = model_form(Graphics)
del GraphicsForm.path