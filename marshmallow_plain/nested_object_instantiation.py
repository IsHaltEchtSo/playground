"""
OBJECTIVE
a POKEMON-object has attacks which are ATTACK-objects
make a dict with a pokemon and attacks and check if a POKEMON object and ATTACK objects are instantiated
"""
from typing import List
from marshmallow import Schema, fields, post_load

class Attack:
    def __init__(self, name:str, strength: int) -> None:
        self.name = name
        self.strength = strength

    def __repr__(self) -> str:
        return f"<Attack {self.name}>"

class Pokemon:
    def __init__(self, name: str, attacks: List[Attack]) -> None:
        self.name = name
        self.attacks = attacks

    def __repr__(self) -> str:
        return f"<Pokemon {self.name} with Attacks {self.attacks}>"

class AttackSchema(Schema):
    name = fields.String()
    strength = fields.Integer()

    @post_load
    def make_attack(self, data, **kwargs):
        return Attack(**data)

class PokemonSchema(Schema):
    class Meta:
        ordered = True

    name = fields.String()
    attacks = fields.List(fields.Nested(AttackSchema()))

    @post_load
    def make_pokemon(self, data, **kwargs):
        return Pokemon(**data)

bubble = Attack(name='Bubble', strength=40)
tackle = Attack(name='Tackle', strength=35)
squirtle = Pokemon(name='Squirtle', attacks=[bubble, tackle])

squirtle_dict = {
    'name': 'Squirtle',
    'attacks': [
        {'name':'Bubble', 'strength':'40'},
        {'name':'Tackle', 'strength':35}
    ]
}

squirtle_serialized = PokemonSchema().dump(squirtle)

squirtle_deserialized = PokemonSchema().load(squirtle_dict)

print(squirtle)
print(squirtle_serialized)
print(squirtle_deserialized)