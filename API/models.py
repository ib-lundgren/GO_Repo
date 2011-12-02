from google.appengine.ext import db

class GameObject(db.Model):
    title = db.StringProperty()
    description = db.TextProperty()
    def to_dict(self):
            d = dict()
            d["id"] = self.key().id()
            for p in self.properties():
              try: 
                d[p] = unicode(getattr(self, p))
              except UnicodeDecodeError as e:
                pass # We add an image url instead
            return d
   
    def __str__(self):
            return str(self.key().id())

class Shape(GameObject):
	width = db.IntegerProperty()
	height = db.IntegerProperty()

class Graphic(GameObject):
    path = db.TextProperty()
    picture = db.BlobProperty(default=None)

class VisualGameObject(GameObject):
	weight = db.FloatProperty()
	#shape = db.ReferenceProperty(Shape)
	graphics = db.ReferenceProperty(Graphic)
	created = db.DateTimeProperty(auto_now_add=True)
	
class CompositeGameObject(GameObject):
	objects = db.ListProperty(db.Key)

class Modifier(GameObject):
	pass

class Environment(VisualGameObject):
	pstates = set(["solid", "liquid", "gas"])
	physical_state = db.StringProperty(choices=pstates)
	lstates = set(["static", "dynamic"])
	location_state = db.StringProperty(choices=lstates)
	interactions = db.ListProperty(db.Key)

class Interaction(GameObject):	
	triggers = set(["enter", "leave", "activate"])
	trigger = db.StringProperty(choices=triggers)
	modifier = db.ReferenceProperty(Modifier)

class Level(GameObject):
	objects = db.ListProperty(db.Key)

class LocatedObject(GameObject):
	x = db.IntegerProperty()
	y = db.IntegerProperty()
	z = db.IntegerProperty()
	obj = db.ReferenceProperty(VisualGameObject)

class Equipment(VisualGameObject):
	pass

class Vehicle(VisualGameObject):
	pass

class Mission(GameObject):
	pass

class Character(VisualGameObject):
	pass

class NPC(VisualGameObject):
	pass

class Team(VisualGameObject):
	pass

class Event(GameObject):
	pass

class Player(GameObject):
	pass

class Game(GameObject):
	pass

