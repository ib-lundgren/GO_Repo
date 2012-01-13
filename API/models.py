from google.appengine.ext import db

# API key management model

class RepoUser(db.Model):
    # Using StringProperty rather than app engine specific for easier
    # portability to Django specific models later
    email = db.StringProperty()
    api_key = db.StringProperty()
    domain = db.StringProperty()


class Secret(db.Model):
    user = db.StringProperty()
    secret = db.StringProperty()

# Game object models

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
            d["key"] = str(self.key())
            d["category"] = str(self.__class__.__name__)
            for p in self.properties():
                try: 
                    d[p] = unicode(getattr(self, p))
                except UnicodeDecodeError as e:
                    pass # We add an image url instead

                # Convert lists of key instances to a list of ids
                if isinstance(getattr(self, p), list):
                    d[p] = [int(i.id()) for i in getattr(self,p)]
                    
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
    graphic = db.ListProperty(db.Key)

class Modifier(GameObject):
    action = db.TextProperty()

class Environment(VisualGameObject):
    physical_state = db.StringProperty()
    location_state = db.StringProperty()
    interactions = db.ListProperty(db.Key)

class Interaction(GameObject):	
    trigger = db.StringProperty()
    action = db.TextProperty()

class Level(GameObject):
    objects = db.ListProperty(db.Key)

class Equipment(VisualGameObject):
    item_type = db.StringProperty()
    item_class = db.StringProperty() # quest, normal, superior etc
    item_value = db.FloatProperty()
    damage = db.FloatProperty()
    armor = db.FloatProperty()
    enhancements = db.ListProperty(db.Key) # modifiers, i.e +hp
        
class Vehicle(VisualGameObject):
    speed = db.FloatProperty()
    acceleration = db.FloatProperty()
    equipment = db.ListProperty(db.Key)
    passengers = db.ListProperty(db.Key)
    drivers = db.ListProperty(db.Key)

class Objective(GameObject):
    goal = db.StringProperty()
    targets = db.ListProperty(db.Key) # npcs usually
    items = db.ListProperty(db.Key) # npcs usually

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
    amount = db.StringProperty() # health, mana etc.

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

class Event(GameObject):
    players = db.ListProperty(db.Key)

class Game(GameObject):
    players = db.ListProperty(db.Key)
    max_players = db.IntegerProperty()
    

