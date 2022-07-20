"""
LEARNINGS
serialize objects to dictionaries, choose which attributes to include/exclude
deserialize objects into dictionaries or objects with @post_load
serialize many objects into a nested dictionary
"""


# LANDING PAGE
from datetime import date
from pprint import pprint
from marshmallow import Schema, fields

class ArtistSchema(Schema):
    name = fields.Str()

class AlbumSchema(Schema):
    title = fields.Str()
    release_date = fields.Date()
    artist = fields.Nested(nested=ArtistSchema())

class Artist:
    def __init__(self, name) -> None:
        self.name = name

bowie = Artist(name='David Bowie')
album = dict(title='Hunky Dory', artist=bowie, release_data=date(year=1971, month=12, day=17))

schema = AlbumSchema()
result = schema.dump(obj=[album, album], many=True)
pprint(result, indent=2)
pprint(album, indent=2)



# DECLARING SCHEMAS
import datetime as dt
from marshmallow import Schema, fields

class User:
    def __init__(self, name, email, **kwargs) -> None:
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()

    def __repr__(self) -> str:
        return f"<User {self.name}>"

class UserSchema(Schema):
    name = fields.Str()
    email = fields.Str()
    created_at = fields.DateTime()



# CREATING SCHEMAS FROM DICTIONARIES (useful for creating schemas on runtime)
UserSchema = Schema.from_dict(
    {'name':fields.Str(), 'email':fields.Str(), 'created_at':fields.DateTime()}
)



# SERIALIZING OBJECTS ("DUMPING")
from pprint import pprint

user_object = User(name='deniz', email='deniz@code.org')
user_schema = UserSchema()
user_serialized = user_schema.dump(user_object)
pprint(user_serialized, indent=2)



# FILTERING OUTPUT
user_schema = UserSchema(only=['name'])
user_serialized = user_schema.dump(user_object)
pprint(user_serialized, indent=2)

user_schema = UserSchema(exclude=['name'])
user_serialized = user_schema.dump(user_object)
pprint(user_serialized, indent=2)



# DESERIALIZING OUTPUT ("LOADING") 
from pprint import pprint

user_data = {
    'name': 'luca',
    'email': 'luca@beach.com',
    'created_at': '2022-07-20T16:33:11.747643'
}

user_schema = UserSchema()
user_deserialized = user_schema.load(user_data)
pprint(user_deserialized, indent=2)



# DESERIALIZING TO OBJECTS
from marshmallow import Schema, fields, post_load

class UserSchema(Schema):
    name = fields.Str()
    email = fields.Str()
    created_at = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

user_schema = UserSchema()
user_object = user_schema.load(user_data)
pprint(user_object, indent=2)



# HANDLING COLLECTIONS OF OBJECTS
deniz = User(name='deniz', email='deniz@beach.org')
luca = User(name='luca', email='luca@beach.org')
user_schema = UserSchema()
user_serialized = user_schema.dump(obj=[deniz, luca], many=True)
pprint(user_serialized, indent=2)