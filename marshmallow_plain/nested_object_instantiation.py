"""
OBJECTIVE
a POKEMON-object has attacks which are ATTACK-objects
make a dict with a pokemon and attacks and check if a POKEMON object and ATTACK objects are instantiated
"""
from marshmallow import Schema, fields, post_load

from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('postgresql+psycopg2://localhost:54321/sqla', echo=False)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

pokemon_attack_association = Table(
    'pokemon_attack_association', Base.metadata,
    Column('pokemon_id', ForeignKey('pokemon.id'), primary_key=True),
    Column('attack_id', ForeignKey('attack.id'), primary_key=True)
)

class Attack(Base):
    __tablename__ = 'attack'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    strength = Column(Integer)
    user = relationship('Pokemon', back_populates='attacks', uselist=False, secondary=pokemon_attack_association)

    def __repr__(self) -> str:
        return f"<Attack {self.name}>"

class Pokemon(Base):
    __tablename__ = 'pokemon'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    attacks = relationship('Attack', back_populates='user', secondary=pokemon_attack_association)

    def __repr__(self) -> str:
        return f"<Pokemon {self.name} with Attacks {self.attacks}>"

Base.metadata.create_all()

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
squirtle_obj = Pokemon(name='Squirtle', attacks=[bubble, tackle])

charmander_dict = {
    'name': 'Charmander',
    'attacks': [
        {'name':'Ember', 'strength':'40'},
        {'name':'Tackle', 'strength':35}
    ]
}

charmander_obj = PokemonSchema().load(charmander_dict)

session = Session()
session.add_all([
    charmander_obj, squirtle_obj
])
session.commit()

pokemon_objects = session.query(Pokemon)
for pokemon_obj in pokemon_objects:
    print(pokemon_obj)  # PRINT THE REPRESENTATION OF THE OBJECTS

for deserialized_pokemon in PokemonSchema().dump(pokemon_objects, many=True):
    print(deserialized_pokemon)  # PRINT THE REPRESENTATION OF THE OBJECT-SCHEMAS