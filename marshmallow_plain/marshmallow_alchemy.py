from marshmallow import Schema, fields
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from flask import Flask, request
from flask_restful import Api, Resource


##### BASIC INITS #####
app = Flask(__name__)
api = Api(app=app)

engine = create_engine('postgresql+psycopg2://deniz@localhost:54321/sqla', echo=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine, expire_on_commit=False)



##### MODELS #####
class Pokemon(Base):
    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    type = Column(String, default='Normal')

Base.metadata.create_all()



##### SCHEMAS #####
class PokemonSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    type = fields.Str()
    pokedex_info = fields.Method('make_pokedex_info', dump_only=True)

    def make_pokedex_info(self, pokemon):
        return f"{pokemon.name} is of type {pokemon.type}"



##### RESOURCES #####
class PokemonView(Resource):
    def get(self):
        session = Session()
        pokemons_schema = PokemonSchema(many=True)
        pokemon_results = session.query(Pokemon).all()
        pokemons = pokemons_schema.dump(pokemon_results)

        return pokemons

    def post(self):
        pokemon_schema = PokemonSchema()
        pokemon_data = pokemon_schema.load(data=request.form)
        pokemon = Pokemon(**pokemon_data)

        session = Session()
        session.add(pokemon)
        session.commit()

        return pokemon_schema.dump(pokemon)

api.add_resource(PokemonView, '/pokemons', endpoint='pokemons_endpoint')

if __name__ == '__main__':
    app.run(debug=True, port=5004)
    # curl localhost:5004/pokemons -X POST -d 'name=.....&type=.....'