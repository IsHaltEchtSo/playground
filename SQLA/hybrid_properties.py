from sqlalchemy import func, create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.ext.hybrid import hybrid_property
# TODO import sql expressions
# from sqlalchemy.sql import 

engine = create_engine('postgresql+psycopg2://deniz@localhost:54321/sqla', echo=False)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine, expire_on_commit=False)

follower_association = Table(
    'follower_association', Base.metadata,
    Column('follower_id', ForeignKey('person.id'), primary_key=True),
    Column('followee_id', ForeignKey('person.id'), primary_key=True)
)

class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    follower = relationship(
        'Person', backref='following', 
        secondary=follower_association,
        primaryjoin=follower_association.c.follower_id == id,
        secondaryjoin=follower_association.c.followee_id == id
    )

    # TODO implement hybrid properties
    # @hybrid_property
    # def follower_count(self):
    #     return len(self.follower)

    # @follower_count.expression
    # def follower_count(cls):
    #     return func.count(cls.follower)

    # @hybrid_property
    # def following_count(self):
    #     return len(self.following)

    def __repr__(self) -> str:
        return f"<Person {self.name}>"

Base.metadata.create_all()

deniz = Person(name='Deniz')
hanna = Person(name='Hanna')
lucas = Person(name='Lucas')
alex = Person(name='Alex')

deniz.follower.extend([alex, hanna, lucas])
hanna.follower.extend([deniz, lucas])
lucas.follower.extend([alex])

session = Session()
session.add(deniz)
session.commit()

persons = session.query(Person)
for person in persons:
    print(f"{person.name} is following {person.following_count} people: {person.following}")
    print(f"{person.name} has {person.follower_count} followers: {person.follower}")

# TODO order persons after follower count
# persons = session.query(Person).order_by().all()

# for p in persons:
#     print(p)