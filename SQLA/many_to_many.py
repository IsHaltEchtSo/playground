from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


engine = create_engine('postgresql+psycopg2://deniz@localhost:54321/sqla', echo=True)
Base = declarative_base(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


class Association(Base):
    __tablename__ = 'association'

    left_id = Column(ForeignKey('left.id'), primary_key=True)
    right_id = Column(ForeignKey('right.id'), primary_key=True)
    extra_data = Column(String(50))
    child = relationship('Child', back_populates='parents')
    parent = relationship('Parent', back_populates='children')

class Parent(Base):
    __tablename__ = 'left'

    id = Column(Integer, primary_key=True)
    children = relationship('Association', back_populates='parent')

class Child(Base):
    __tablename__ = 'right'

    id = Column(Integer, primary_key=True)
    parents = relationship('Association', back_populates='child')

Base.metadata.create_all()

p = Parent()
c1 = Child()
c2 = Child()
a1 = Association(extra_data='some')
a2 = Association(extra_data='more')

a1.child = c1
a2.child = c2
p.children.extend([a1, a2])

session.add(p)
session.commit()

parent_query = session.query(Parent).scalar()

for assoc in parent_query.children:
    print(assoc.extra_data)
    print(assoc.child)
    print(assoc.parent)
    print('===')

