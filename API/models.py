from google.appengine.ext import db

class VisualGameObject(db.Model):
	# id is automatic, no need for explicit field
	weight = db.FloatProperty()
	height = db.FloatProperty()
	shape = db.ReferenceProperty(Shape)
	graphics = db.ReferenceProperty(Graphics)
	created = db.DateTimeProperty(auto_add_now=true)

class CompositeGameObject(db.Model):
	objects = db.ListProperty(db.Key)

class Shape(db.Model):
	pass

class Graphics(db.model):
	pass

class Environment(VisualGameObject):
	pstates = set(["solid", "liquid", "gas"])
	physical_state = db.StringProperty(choices=pstates)
	lstates = set(["static", "dynamic"])
	location_state = db.StringProperty(choices=lstates)
	interactions = db.ListProperty(db.Key)

class Interaction(db.Model):
	triggers = set(["enter", "leave", "activate"])
	trigger = db.StringProperty(choices=triggers)
	modifier = db.ReferenceProperty(Modifier)

class Modifier(db.Model):
	pass

class Level(db.Model):
	objects = db.ListProperty(db.Key)

class LocatedObject(db.Model):
	x = db.IntegerProperty()
	y = db.IntegerProperty()
	z = db.IntegerProperty()
	obj = ReferenceProperty(VisualGameObject)

# todo: add more properties and classes
