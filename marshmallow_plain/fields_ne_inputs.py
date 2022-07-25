from marshmallow import Schema, fields, post_load
from pprint import pprint

class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

class PersonSchema(Schema):
    name = fields.String()
    age = fields.Integer()

    @post_load
    def make_person(self, data, **kwargs):
        return Person(**data)

too_many_inputs = {'name':'deniz', 'age':26, 'location':'berlin'}
not_enough_inputs = {'name':'deniz'}

too_many_error = PersonSchema().validate(data=too_many_inputs)  # VALIDATION FAILS BECAUSE 'LOCATION' IS AN UNKNOWN FIELD
not_enough_error = PersonSchema().validate(data=not_enough_inputs)  # VALIDATION IS OK BECAUSE POST_LOAD IS NOT VALIDATED

pprint(too_many_error)
pprint(not_enough_error)

deniz = PersonSchema().load(data=not_enough_inputs)  # FAILS BECAUSE THE PERSON-CONSTRUCTOR NEEDS AN 'AGE' KWARG
pprint(deniz)