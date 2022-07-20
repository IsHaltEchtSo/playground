from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('postgresql+psycopg2://deniz@localhost:54321/sqla', echo=True)

Session = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base(bind=engine)

class IceCream(Base):
    __tablename__ = 'ice_cream'

    id = Column(Integer, primary_key=True)
    flavor = Column(String)
    price = Column(Float, default=0.99)

Base.metadata.create_all()



from flask import Flask, request
from flask_restful import Api, Resource, marshal_with, fields

ice_cream_marshal_plan = {
    'id': fields.Integer,
    'flavor': fields.String,
    'price': fields.Float
}

app = Flask(__name__)
api = Api(app=app)

class IceCreamList(Resource):
    @marshal_with(fields=ice_cream_marshal_plan)
    def get(self, ice_cream_id):
        session = Session()
        icecream = session.query(IceCream).filter(IceCream.id.__eq__(ice_cream_id)).scalar()

        return icecream

    @marshal_with(fields=ice_cream_marshal_plan)
    def post(self, **kwargs):
        flavor = request.form['flavor']
        new_ice_cream = IceCream(flavor=flavor)

        session = Session()
        session.add(new_ice_cream)
        session.commit()

        return new_ice_cream

request_marshal_plan = {'name': fields.String, 'age': fields.Integer}

class RequestParser(Resource):
    @marshal_with(fields=parser_fields)
    def post(self):
        form = request.form

        return form



api.add_resource(IceCreamList, '/ice_cream_list/<int:ice_cream_id>', endpoint='ice_cream_list')
api.add_resource(RequestParser, '/req', endpoint='request_parser')

if __name__ == '__main__':
    app.run(debug=True, port=5001)