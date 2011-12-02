from wtforms.ext.appengine.db import model_form
from models import *
from copy import copy

GameObjectForm = model_form(GameObject)
VisualGameObjectForm = model_form(VisualGameObject)
EnvironmentForm = model_form(Environment)

BaseGraphicForm = model_form(Graphic)
del BaseGraphicForm.path

class GraphicForm(BaseGraphicForm):
  formdata = None
  
  def __init__(self, data=None):
    self.formdata = copy(data)
    if data:
      data["picture"] = ""
    super(GraphicForm,self).__init__(data)

  def populate_obj(self, obj):
    if self.formdata:
      content = self.formdata.get("picture")
      if content:
        obj.picture = content.read()
      obj.save() # create ID
      obj.path = "api/images/" + str(obj.key().id())
      # tmp--
      obj.description = self.formdata.get("description")
      obj.title = self.formdata.get("title")
      #super(GraphicsForm,self).populate_obj(obj)
    
      
