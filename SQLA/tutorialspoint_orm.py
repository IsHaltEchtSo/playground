"""
LEARNINGS

mapping used to create objects that represent rows of a table
a session is an adapter that communicates between programm and database
every session has its own flush-deposit and transactions can only be viewed from other sessions upon commiting them/storing them persistent on disk
the query object is a select statement that can be further adjusted (filter, update, delete, group, ...)
the result of a query is either a list of scalars or a scalar
textual sql can be used in sql expressions, also with bound parameters
relationship-construct creates an attribute to access objects from linked tables (via pkey) 
as long as objects are connected via a relationship-attribute it doesn't matter which object you add/commit via session
"""

# DECLARE MAPPING
"""
describe the database tables, then match them with classes
declarative system automatically maps classes to the db tables
declarative base is a catalog of classes and tables mapped together
the metadata object is stored inside of the base as well
"""
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine

engine = create_engine('postgresql+psycopg2://deniz@localhost:54321/sqla', echo=True)

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base(engine)

class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    address = Column(String)

Base.metadata.create_all()


# CREATING SESSION
"""
to interact with the db, establish a connection by opening a session
session.begin/add/add_all/delete/commit/flush/rollback/execute/expire/close/invalidate
"""
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
session2 = Session()


# ADDING OBJECTS
c1 = Customers(name='Denniz', age=26, address='Berlin')
session.add(c1)

session.add_all([
    Customers(name='Lucas', age=23, address='Raunheim'),
    Customers(name='Timbo', age=28, address='Rüsselsheim')
])

q = session.query(Customers).where(Customers.age == 28).all()
q2 = session2.query(Customers).where(Customers.age == 28).all()  # CAN'T ACCESS CHANGES OF QUERY1 THAT HAVEN'T BEEN COMMITED TO THE DB YET
print('q')
for row in q:
    print(row.name, row.age, row.address)
print('q2')
for row in q2:
    print(row.name, row.age, row.address)

session.commit()


# USING QUERY
"""
query(Customers).add_columns/add_entitiy/count/delete/distinct/filter/first/get/group_by/join/one/order_by/update
"""
result = session.query(Customers).all()

for row in result:
    print(f"The Customer {row.name} is {row.age} years old and lives in {row.address}.")


# UPDATING OBJECTS
ninenine = session.query(Customers).get(2)
ninenine.age = 999
session.commit()

session.query(Customers).where(Customers.name.ilike('dENiz')).update(
    {Customers.address:'Berlin, Raunheim'}, 
    synchronize_session=False    
)

session.commit()


# FILTER WITH ILIKE, IN, AND, OR
from sqlalchemy import or_, and_
r = session.query(Customers).filter(
    or_(
        Customers.name.ilike('%denn%'), 
        Customers.id.in_([15,65,987]),
        and_(
            Customers.age.between(cleft=99, cright=99), 
            Customers.name.like('Timb%')
        )
    )
)

for row in r:
    print(row.id, row.name, row.age, row.address)


# RETURNING SCALARS AND LISTS
# .all(), .first(), .one(), .scalar()
r = session.query(Customers).filter(Customers.id == 1)  # RETURNS A LIST OF OBJECTS, OF SCALARS
r2 = session.query(Customers).filter(Customers.id == 1).scalar()  # RETURNS THE OBJECT, A SCALAR


# TEXTUAL SQL
# Using the text-constructor allows creating textual sql that can be used in most sql-expressions
from sqlalchemy import text
r = session.query(Customers).where(text('id < 5'))

for row in r:
    print(row.id, row.name)

r = session.query(Customers).from_statement(text("SELECT id, name FROM customers WHERE id < 10"))
for row in r:
    print(row.id, row.name)

r = session.query(Customers).filter(text('id < :idd').params(idd=4))
for row in r:
    print(row.id, row.name)



# BUILDING RELATIONSHIP
from sqlalchemy.orm import relationship

class Athlete(Base):
    __tablename__ = 'athlete'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    discipline = Column(String)
    equipment = relationship('Equipment', back_populates='athlete')

class Equipment(Base):
    __tablename__ = 'equipment'

    id = Column(Integer, primary_key=True)
    athlete_id = Column(Integer, ForeignKey('athlete.id'))  # THIS IS THE 'ONE' SIDE
    name = Column(String)
    athlete = relationship('Athlete', back_populates='equipment')
    
Base.metadata.create_all()



# WORKING WITH RELATED OBJECTS
racket = Equipment(name='Tennis Racket')
nadal = Athlete(name='Nadal', discipline='Tennis', equipment=[racket])

session.add(nadal)
session.commit()

messi = Athlete(name='Messi', discipline='Soccer')
messi.equipment.extend([
    Equipment(name='Soccer clets'),
    Equipment(name='Soccer Jersey')
])

session.add(messi)
session.commit()

sorum = Athlete(name='Sorum', discipline='Beach Volleyball', equipment=[
    Equipment(name='Volleyball'), Equipment(name='Jersey')
])

session.add(sorum)
session.commit()

klitschko = Athlete(name='Klitschko', discipline='Boxing')
gloves = Equipment(name='Boxing Gloves', athlete=klitschko)

session.add(gloves)
session.commit()

milo = Athlete(name='Milo', discipline='Wrestling')
pants = Equipment(name='Wrestling Pants', athlete=milo)

session.add(milo)
session.commit()

tennis_results = session.query(Athlete).filter(Athlete.discipline.ilike('soccer'))

for athlete in tennis_results:
    print(f"The athlete {athlete.name} plays {athlete.discipline}")
    print(f"He uses the following equipment:")
    for equipment in athlete.equipment:
        print(f"-- {equipment.name}")