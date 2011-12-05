from google.appengine.ext import db

class GameObject(db.Model):
    title = db.StringProperty()
    description = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    rating = db.RatingProperty(default=0)
    downloads = db.IntegerProperty(default=0)
    votes = db.IntegerProperty(default=0)
    extra = db.TextProperty()
    
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

class Graphic(GameObject):
    path = db.TextProperty()
    picture = db.BlobProperty(default=None)

class VisualGameObject(GameObject):
    weight = db.FloatProperty()
    width = db.FloatProperty()
    height = db.FloatProperty()
    graphics = db.ReferenceProperty(Graphic)

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
    types = set(["weapon", "armor", "consumable", "other"]) # add more
    item_type = db.StringProperty(choices=types)
    item_class = db.StringProperty() # quest, normal, superior etc
    value = db.FloatProperty()
    damage = db.FloatProperty()
    max_damage = db.FloatProperty()
    min_damage = db.FloatProperty()
    armor = db.FloatProperty()
    shot_range = db.FloatProperty()
    enhancements = db.ListProperty(db.Key) # modifiers, i.e +hp
        
class Vehicle(VisualGameObject):
    speed = db.FloatProperty()
    acceleration = db.FloatProperty()
    equipment = db.ListProperty(db.Key)
    passengers = db.ListProperty(db.Key)
    drivers = db.ListProperty(db.Key)

class Objective(GameObject):
    goals = set(["collect", "kill", "activate", "defend"])
    goal = db.StringProperty(choices=goals)
    targets = db.ListProperty(db.Key) # npcs usually

class Mission(GameObject):
    objectives = db.ListProperty(db.Key)
    rewards = db.ListProperty(db.Key) # equipment usually
    pre_required = db.ListProperty(db.Key) # earlier missions
    follow_up = db.ListProperty(db.Key) # new missions

class Team(GameObject):
    members = db.ListProperty(db.Key) # npcs and characters
    enemies = db.ListProperty(db.Key) # other teams

class Skill(GameObject):
    rank = db.FloatProperty()
    
class Attribute(GameObject):
    value = db.FloatProperty() # health, mana etc.

class NPC(VisualGameObject):
    skills = db.ListProperty(db.Key) 
    attributes = db.ListProperty(db.Key) # age, level, hp, strength, race
    equipment = db.ListProperty(db.Key)
    missions = db.ListProperty(db.Key)
    teams = db.ListProperty(db.Key)
    
class Character(NPC):
    pass

class Player(GameObject):
    characters = db.ListProperty(db.Key)
    friends = db.ListProperty(db.Key) # other players
    played = db.FloatProperty() # hours wasted :P

class Event(GameObject):
    player = db.ReferenceProperty(Player)

class Game(GameObject):
    players = db.ListProperty(db.Key)
    max_players = db.IntegerProperty()
    

