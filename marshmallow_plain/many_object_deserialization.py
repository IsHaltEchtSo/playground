from pprint import pprint
from marshmallow import Schema, fields, post_load

class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        return f"<Person {self.name}>"

class PersonSchema(Schema):
    name = fields.String()
    age = fields.Integer()

    @post_load
    def make_person(self, data, **kwargs):
        return Person(**data)

persons_data = [
    {'name':'deniz', 'age':26},
    {'name':'hanna', 'age': 21}
]

persons = PersonSchema().load(data=persons_data, many=True)
for person in persons:
    pprint((person, person.name, person.age), indent=2)