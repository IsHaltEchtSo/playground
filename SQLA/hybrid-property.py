"""
Test the difference between @property and @hybrid_property
Hunch: the hybrid_property can be accessed in queries as well
--> Hybrid_properties are translated into sql-expressions for querying while normal properties only work on the instance level
"""
from enum import Enum
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

class Pets(str, Enum):
    DOG = "dogG"
    CAT = 'Cat'

class FerociousAnimals(str, Enum):
    LION = 'Lion'
    TIGER = 'Tiger'
    FOX = 'Fox'

class Status(str, Enum):
    PRESENT = 'PRESENT'
    SOLD = 'SOLD'
    HOLD = 'HOLD'

engine = create_engine('postgresql+psycopg2://deniz@localhost:54321/sqla', echo=False)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

class Animal(Base):
    __tablename__ = 'animal'
    id = Column(Integer, primary_key=True)
    race = Column(String, default='DOG')

    def __init__(self, race):
        self.race = race

    @property
    def is_pet(self):
        return self.race == 'DOG'

    @hybrid_property
    def is_ferocious_animal(self):
        return self.race == 'FOX'

    @hybrid_property
    def status(self):
        if self.race:
            return Status.PRESENT if self.race else Status.SOLD
        return Status.HOLD

    def __repr__(self) -> str:
        return f"<Animal {self.race}>"

Base.metadata.create_all()

cap = Animal(race='FOX')
capper = Animal(race='DOG')

session = Session()
session.add_all([
    cap, capper
])
session.commit()

# TEST 1: DO IS_PET/IS_FEROCIOUS_ANIMAL WORK AS INTENDED?
print(f"Cap is pet: {cap.is_pet} and is ferocious animal: {cap.is_ferocious_animal}")
print(f"Capper is pet: {capper.is_pet} and is ferocious animal: {capper.is_ferocious_animal}")

# TEST 2: IS THERE A DIFFERENCE TO PROPERTY/HYBRID_PROPERTY WHEN FILTERING?

# pets = session.query(Animal).filter(Animal.is_pet)  DOES NOT WORK BECAUSE THE PROPERTY DOESN'T TRANSLATE TO A SQL-EXPRESSION
# for pet in pets:
#     print(pet)
animals = session.query(Animal).filter(Animal.is_ferocious_animal == True)  # WORKS BECAUSE THE HYBRID-PROPERTY TRANSLATES TO A SQL-EXPRESSION
for animal in animals:
    print(animal)

animals = session.query(Animal).filter(Animal.status == Status.PRESENT)
for animal in animals:
    print(f"The animal {animal.race} is {animal.status}")



# HYBRID ATTRIBUTES FROM SQLA
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property

class Interval(Base):
    __tablename__ = 'interval'

    id = Column(Integer, primary_key=True)
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)

    def __init__(self, start, end):
        self.start = start
        self.end = end

    @hybrid_property
    def length(self):
        return self.end - self.start

    @hybrid_method
    def contains(self, point):
        return (self.start <= point) & (point <= self.end)

    @hybrid_method
    def intersects(self, other):
        """Return if they intersect, not if one is a subset of the other"""
        return self.contains(other.start) | self.contains(other.end)

    def __repr__(self) -> str:
        return f"<Interval {self.start}:{self.end}>"

Base.metadata.create_all()

one_to_ten = Interval(start=1, end=10)
print(one_to_ten.length)

session.add(one_to_ten)
session.commit()

small_intervals = session.query(Interval).filter(Interval.length > 1)
for i in small_intervals:
    print(i)