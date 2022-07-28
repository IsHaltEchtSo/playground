"""
LEARNINGS
to use hybrid_properties for queries, use func.expression and pass it some query written in SQL Expression Language
"""
from typing_extensions import Self
from sqlalchemy import \
    create_engine, Column, Integer, String, Table, ForeignKey, \
    desc, asc, select, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

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
        primaryjoin=follower_association.c.followee_id == id,
        secondaryjoin=follower_association.c.follower_id == id
    )

    @hybrid_property
    def follower_count(self):
        return len(self.follower)

    @follower_count.expression
    def follower_count(cls):
        return select([func.count()]) \
            .where(cls.id == follower_association.c.followee_id) \
            .scalar_subquery()

    @hybrid_property
    def following_count(self):
        return len(self.following)

    @following_count.expression
    def following_count(cls):
        return select([func.count()]) \
            .where(cls.id == follower_association.c.follower_id) \
            .scalar_subquery()

    @hybrid_method
    def has_follower(self, follower: Self) -> bool:
        for p in self.follower:
            if p.id == follower.id:
                return True
        return False

    @has_follower.expression
    def has_follower(cls, follower: Self.__class__):
        return select(bool(1)) \
                .where(cls.id == follower_association.c.followee_id) \
                .where(follower.id == follower_association.c.follower_id) \
                .scalar_subquery()

    def __repr__(self) -> str:
        return f"<Person {self.name}>"

Base.metadata.create_all()

deniz = Person(name='Deniz')
hanna = Person(name='Hanna')
lucas = Person(name='Lucas')
alex = Person(name='Alex')
danny = Person(name='Danny')
paul = Person(name='Paul')

deniz.follower.extend([alex, hanna, lucas, danny, paul])
hanna.follower.extend([deniz, lucas])
lucas.follower.extend([alex, danny])
danny.follower.extend([alex])

session = Session()
session.add(deniz)
session.commit()

print(f"{hanna} has follower {alex}: {hanna.has_follower(alex)}")

has_alex = session.query(Person).filter(Person.has_follower(alex))
for p in has_alex:
    print(f"{p} has a follower in alex")

persons = session.query(Person)
for person in persons:
    print(f"{person.name} is following {person.following_count} people: {person.following}")
    print(f"{person.name} has {person.follower_count} followers: {person.follower}")

followees = session.query(Person).order_by(desc(Person.follower_count)).all()

for p in followees:
    print(f"{p} has {p.follower_count} followers and is following {p.following_count} people.")

print('#'*20)
followers = session.query(Person).order_by(asc(Person.following_count), ).all()

for p in followers:
    print(f"{p} is following {p.following_count} people and has {p.follower_count} followers.")