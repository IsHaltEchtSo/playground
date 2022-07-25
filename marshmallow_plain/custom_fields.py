"""
THREE WAYS TO ADD CUSTOM FIELDS
create a field class - inherit from fields.Field and implement _serialize/_deserialize
use a field method - use fields.Method() with serialize/deserialize parameters
use a field function - use fields.Function() with serialize/deserialize parameters
to create custom error message, use error_messages parameter for the field or inherit from the field's class and use the default_error_messages property
"""

# CREATING A CUSTOM FIELD CLASS
from datetime import datetime as dt
from marshmallow import Schema, fields, ValidationError

class PinCode(fields.Field):
    """
    Field that serialized to a string of numbers and deserializes to a list of numbers
    ['1', '2'] , [1, 2]
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return "".join(str(digit) for digit in value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return [int(character) for character in value]
        except ValueError as err:
            raise ValidationError(message="Pin Codes must contain only numbers") from err

class UserSchema(Schema):
    name = fields.String()
    email = fields.Email()
    created_at = fields.DateTime()
    pin_code = PinCode()

user_dict = {'name':'deniz', 'email':'deniz@beachen.org', 'created_at':dt.now().isoformat(), 'pin_code':'465478'}

user_deserialized = UserSchema().load(user_dict)
user_serialized = UserSchema().dump(user_deserialized)
print(user_deserialized)
print(user_serialized)



# USING METHOD FIELDS
class UserSchema(Schema):
    name = fields.String()
    email = fields.Email()
    created_at = fields.DateTime()
    since_created = fields.Method(serialize="get_days_since_created", deserialize='get_day_since_created')

    def get_days_since_created(self, obj):
        return dt.now().day - obj['created_at'].day

    def get_day_since_created(self, value):
        return int(value)

user_dict = {'name':'deniz', 'email':'deniz@beachen.org', 'created_at':dt(2022,7,13).isoformat(), 'since_created':12}

user_deserialized = UserSchema().load(user_dict)
user_serialized = UserSchema().dump(user_deserialized)

print(user_deserialized)
print(user_serialized)



# USING FIELD FUNCTIONS
class UserSchema(Schema):
    name = fields.String()
    email = fields.Email()
    created_at = fields.DateTime()
    uppername = fields.Function(serialize=lambda obj: obj['name'].upper(), deserialize=lambda value: value.upper())

user_dict = {'name':'deniz', 'email':'deniz@beachen.org', 'created_at':dt.now().isoformat(), 'uppername':'deniz'}

user_deserialized = UserSchema().load(user_dict)
user_serialized = UserSchema().dump(user_deserialized)

print(user_deserialized)
print(user_serialized)



# CUSTOMIZING ERROR MESSAGES

class MyEmail(fields.Email):
    default_error_messages = {"invalid": "yooooo, do you know how an email looks like??"}

class PersonSchema(Schema):
    name = fields.String()
    email = MyEmail()
    age = fields.Integer(required=True, error_messages={'invalid': 'yooo make it a number, baaaka'})

person_dict = {'name':'deniz', 'email':'yoo', 'age':'yoo'}

errors = PersonSchema().validate(person_dict)
print(errors)



# ADDING CONTEXT TO METHOD AND FUNCTION FIELDS
class UserSchema(Schema):
    name = fields.String()
    # Function fields optionally receive context argument
    is_author = fields.Function(lambda obj, context: obj == context['blog'].author)
    likes_bikes = fields.Method(serialize='writes_about_bikes')

    def writes_about_bikes(self, obj):
        return 'bicycle' in self.context['blog'].title.lower()

schema = UserSchema()

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self) -> str:
        return f"<User {self.name}>"

class Blog:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __repr__(self) -> str:
        return f"<Blog {self.title}>"

schema = UserSchema()

fred = User(name='Freddy Mercury', email='fred@queen.org')
bicycle_blog = Blog(title='Bicycle Blog', author=fred)

schema.context = {'blog': bicycle_blog}
fred_serialized = schema.dump(fred)
print(fred_serialized['is_author'])
print(fred_serialized['likes_bikes'])