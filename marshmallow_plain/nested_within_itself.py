from pprint import pprint
from sqlalchemy import Table, ForeignKey, Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('postgresql+psycopg2://deniz@localhost:54321/sqla', echo=False)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

friends_association = Table(
    'friends_association', Base.metadata,
    Column('person1_id', ForeignKey('person.id'), primary_key=True),
    Column('person2_id', ForeignKey('person.id'), primary_key=True)
)

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    friends = relationship('Person', back_populates='friends', secondary=friends_association,
                            primaryjoin=friends_association.c.person1_id == id,
                            secondaryjoin=friends_association.c.person2_id == id
    )

    def __repr__(self) -> str:
        return f"<Person {self.name}>"
# TODO: explain and draw what happens with one table many to many association

Base.metadata.create_all()

ben = Person(name='Ben')
deniz = Person(name='Deniz')
paul = Person(name='Paul')

deniz.friends.extend([ben, paul])

session = Session()
session.add(deniz)
session.commit()



from marshmallow import Schema, fields

class PersonSchema(Schema):
    name = fields.String()
    friends = fields.List(fields.Nested('PersonSchema', exclude=('friends',)))

persons = session.query(Person)
for person in persons:
    print((f"Person {person.name} is friends with {person.friends}"))


deniz_obj = session.query(Person).filter(Person.name.ilike("deniz")).first()
deniz_serialized = PersonSchema().dump(deniz_obj)
pprint(deniz_serialized, indent=2)