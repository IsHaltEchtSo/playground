"""
LEARNINGS
serialize objects to dictionaries, choose which attributes to include/exclude
deserialize objects into dictionaries or objects with @post_load
serialize many objects into a nested dictionary
objects to be serialized can be of different types
marshmallow only serializes the fields specified; additional ones are omitted, missing ones are left out
validation happens when data is deserialized by a schema and should happen in a try/except block
load_default / dump_default provide default values for deserialization/serialization
"""


# FROM THE LANDING PAGE
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
    def __init__(self, name: str, email: str, **kwargs) -> None:
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
    email = fields.Email()
    created_at = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs) -> User:
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



# FROM OBJ TO DICT
class Hardware:
    def __init__(self, name: str, type: str, price: float) -> None:
        self.name = name
        self.type = type
        self.price = price  # THIS WON'T BE EXTRACTED BY THE HARDWARE SCHEMA

    def __repr__(self) -> str:
        return f"<{self.type} {self.name}>"

class HardwareSchema(Schema):
    """
    Given some input object/dict, the schema only extracts the values for keys that are identical to its attributes
    """
    name = fields.Str()
    type = fields.Str()
    goal = fields.Str()  # THIS WON'T EXTRACT ANYTHING

    @post_load
    def make_hardware(self, data, **kwargs) -> Hardware:
        return Hardware(**data, price=100)

iPhone = Hardware(name='iPhone', type='Smartphone', price=649.50)
magic_mouse = dict(name='Magic Mouse', type='Bluetooth Mouse', price=114.90, alias='super mouse')

hardware_schema = HardwareSchema()
hardware_serialized = hardware_schema.dump(obj=[iPhone, magic_mouse], many=True)
pprint(hardware_serialized, indent=2)
hardware_deserialized = hardware_schema.load(hardware_serialized, many=True)
pprint(hardware_deserialized, indent=2)



# VALIDATION
from marshmallow import Schema, fields, ValidationError, validate, validates

try:
    user_object = UserSchema().load({'name':'Lin', 'email':'lin'})
except ValidationError as err:
    pprint(err.messages)  # THE EMAIL IS NOT VALID
    pprint(err.valid_data)  # THE NAME IS VALID

class BandMemberSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email()

band_data = [
    {"name": "Den", "email": 'den@rock.org'},
    {'name': 'Luca', 'email': 'invalid_email'},  # INVALID EMAIL
    {'name': 'Lin', 'email': 'lin@rock.org'},
    {'email': 'akhil@rock.org'}  # INVALID NAME
]

try:
    BandMemberSchema().load(band_data, many=True)
except ValidationError as err:
    pprint(err.messages, indent=2)
    pprint(err.valid_data, indent=2)

class UserSchema(Schema):
    name = fields.String(validate=validate.And(validate.Length(min=2), validate.Length(max=10)))
    permission = fields.String(validate=validate.OneOf(['read', 'write', 'admin']))
    age = fields.Integer(validate=validate.Range(min=18, max=50))

user_data = {'name':'', 'permission':'delete', 'age':72}

try:
    UserSchema().load(user_data)
except ValidationError as err:
    pprint(err.messages, indent=2)
    pprint(err.valid_data)

class ItemSchema(Schema):
    def validate_quantity(n):  # A CUSTOM VALIDATOR
        if n <= 0:
            raise ValidationError(message='Quantity must be greater than 0')
        if n > 30:
            raise ValidationError(message='Quantity must not be greater than 30')

    def validate_15(n):  # A CUSTOM VALIDATOR
        if n != 15:
            raise ValidationError(message='Quantity is not 15!')

    quantity = fields.Integer(validate=[validate_quantity, validate_15])
    price = fields.Integer()

    @validates(field_name='price')
    def check_price(self, price):  # A METHOD FOR FIELD VALIDATION
        if price > 500:
            raise ValidationError(message="The item's price may not exceed 500€")
        if price < 10:
            raise ValidationError(message='The item should cost at least 10€')

item_data = [
    {'quantity': 31},
    {'quantity': -1},
    {'quantity': 15}
]

try: 
    ItemSchema().load(item_data, many=True)
except ValidationError as err:
    pprint(err.messages, indent=2)
    pprint(err.valid_data, indent=2)



# SPECIFYING DEFAULTS
import uuid
class UserSchema(Schema):
    id = fields.UUID(load_default=uuid.uuid1)
    birthdate = fields.DateTime(dump_default=dt.datetime(year=1995, month=12, day=13))

pprint(UserSchema().load({}))
pprint(UserSchema().dump({}))



# HANDLING UNKNOWN FIELDS
from marshmallow import INCLUDE, EXCLUDE
class User:
    def __init__(self, id, name, age) -> None:
        self.id = id
        self.name = name
        self.age = age

class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()

user_data = {'id':1, 'name':'deniz', 'age':15}
user_object = User(id=2, name="deniz", age=17)

user_deserialized_include = UserSchema().load(user_data, unknown=INCLUDE)
user_deserialized_exclude = UserSchema().load(user_data, unknown=EXCLUDE)
pprint(user_deserialized_include, indent=2)
pprint(user_deserialized_exclude, indent=2)

user_serialized = UserSchema().load(user_object.__dict__, unknown=INCLUDE)
pprint(user_serialized, indent=2)



# VALIDATION WITHOUT DESERIALIZATION
errors = ItemSchema().validate({'quantity':140, 'price':5})
pprint(errors)



# 'READ-ONLY' AND 'WRITE-ONLY' FIELDS
class UserSchema(Schema):
    class Meta:
        ordered = True

    name = fields.String()
    password = fields.String(load_only=True)
    created_at = fields.DateTime(dump_only=True)

user_dict = {'name':'deniz', 'password':'super_tricky+password', 'created_at':dt.datetime.now()}

pprint(UserSchema().load(user_dict, unknown=INCLUDE))
pprint(UserSchema().dump(user_dict))




# SCHEMA-LEVEL VALIDATION
from marshmallow import validates_schema

class OlderBrotherSchema(Schema):
    name = fields.String()
    age = fields.Integer()
    sibling_name = fields.String()
    sibling_age = fields.Integer()

    @validates_schema
    def needs_younger_brother(self, data, **kwargs):
        if not data['sibling_name']:
            raise ValidationError(message='An older brother needs a younger sibling!')
    
    @validates_schema
    def needs_to_be_older(self, data, **kwargs):
        if data['age'] < data['sibling_age']:
            raise ValidationError(message='The older brother needs to be older than the sibling!')

older_brother_data = {'name':'deniz', 'age':26, 'sibling_name':'domi', 'sibling_age':25}

not_older_brother_data = {'name': 'domi', 'age':25, 'sibling_name':'deniz', 'sibling_age':26}

errors = OlderBrotherSchema().validate(data=[older_brother_data, not_older_brother_data], many=True)
pprint(errors, indent=2)
