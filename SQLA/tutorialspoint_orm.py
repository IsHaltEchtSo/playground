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
joins are great to retrieve pairs of rows but accessing the relationship-attribute is more suited to see all related rows to one row
subqueries, functions and joins are used to create sophisticaed queries
lazy load for in-time loading of associated rows, eager load to query all associated rows beforehand
define the cascading type in relationship to configure how deletes/updates/... propagate to related objects
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

    def __repr__(self) -> str:
        return f"<Athlete {self.name}>"

class Equipment(Base):
    __tablename__ = 'equipment'

    id = Column(Integer, primary_key=True)
    athlete_id = Column(Integer, ForeignKey('athlete.id'))  # THIS IS THE 'ONE' SIDE
    name = Column(String)
    price = Column(Integer, default=550)
    athlete = relationship('Athlete', back_populates='equipment')

    def __repr__(self) -> str:
        return f"<Equipment {self.name}>"
    
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

schumacher = Athlete(name='Schumacher', discipline='Formula One')

session.add(schumacher)
session.commit()

tennis_results = session.query(Athlete).filter(Athlete.discipline.ilike('soccer'))

for athlete in tennis_results:
    print(f"The athlete {athlete.name} plays {athlete.discipline}")
    print(f"He uses the following equipment:")
    for equipment in athlete.equipment:
        print(f"-- {equipment.name}")



# WORKING WITH JOINS
from sqlalchemy.sql import func
for a, e in session.query(Athlete, Equipment).filter(Athlete.id == Equipment.athlete_id).all():
    print("{} has {}".format(a, e))

equipment_count_subquery = session.query(
    Equipment.athlete_id, func.count('*').label('equipment_count')
    ).group_by(Equipment.athlete_id).subquery()

for athlete, equip_count in session.query(Athlete, equipment_count_subquery.c.equipment_count).outerjoin(equipment_count_subquery, Athlete.id == equipment_count_subquery.c.athlete_id):
    print(f"{athlete} {equip_count}")



# COMMON RELATIONSHIP OPERATORS
wrestling_pants_query = session.query(Equipment).filter(Equipment.name.__eq__('Wrestling Pants'))
not_wrestling_pants_query = session.query(Equipment).filter(Equipment.name.__ne__('Wrestling Pants'))

for equipment in wrestling_pants_query:
    print(equipment)

for equipment in not_wrestling_pants_query:
    print(equipment)

ten_athletes = session.query(Athlete).filter(Athlete.discipline.contains('Ten'))  # SAME AS LIKE('%...%)

for athlete in ten_athletes:
    print(athlete)

any_athlete_with_550_equipment = session.query(Athlete).filter(Athlete.equipment.any(Equipment.price.__eq__(550)))  # ANY IS USED FOR THE ONE SIDE TO RETRIEVE ANY OF ITS OBJECTS

for athlete in any_athlete_with_550_equipment:
    print(athlete)

equipment_has_athlete = session.query(Equipment).filter(Equipment.athlete.has(Athlete.name.__ne__('Messi')))  # HAS IS USED FOR THE MANY SIDE TO RETRIEVE THE ONE OBJECT EVERY MANY HAS

for equipment in equipment_has_athlete:
    print(equipment)



# EAGER LOADING
from sqlalchemy.orm import eagerload
session_new = Session()

lazy_athletes = session_new.query(Athlete).options()

print('\n\nTHIS IS LAZY LOADING\n\n')
for athlete in lazy_athletes:
    print(athlete.equipment)

session_new = Session()

eager_athletes = session_new.query(Athlete).options(eagerload(Athlete.equipment))

print('\n\nTHIS IS EAGER LOADING\n\n')
for athlete in eager_athletes:
    print(athlete.equipment)



# DELETING RELATED OBJECTS
from sqlalchemy import Table
child_toy_association = Table(
    'child_toy_association', 
    Base.metadata,
    Column('child_id', ForeignKey('child.id'), primary_key=True),
    Column('toy_id', ForeignKey('toy.id'), primary_key=True)
)

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    toys = relationship('Toy', back_populates='children', secondary=child_toy_association, cascade='all')

class Toy(Base):
    __tablename__ = 'toy'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    children = relationship('Child', back_populates='toys', secondary=child_toy_association)

Base.metadata.create_all()

billy = Child(name='Billy')
luis = Child(name='Luis')

truck = Toy(name='Truck')
shovel = Toy(name='Shovel')

billy.toys.append(truck)
luis.toys.append(shovel)

session.add_all([billy, luis])
session.commit()

session.delete(billy)  # ALSO DELETES THE TRUCK
session.delete(shovel)  # DOES NOT DELETE LUIS
session.commit()



# MANY TO MANY RELATIONSHIPS