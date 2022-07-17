from sqlalchemy import ForeignKey, Integer, String, Table, create_engine, Column
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('postgresql+psycopg2://deniz@localhost:54321/sqla', echo=False)

Base = declarative_base(bind=engine)

association_table = Table(
    "association",
    Base.metadata,
    Column('student_id', ForeignKey('student.id')),
    Column('module_id', ForeignKey('module.id')),
)


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    modules = relationship("Module", back_populates='students', secondary=association_table)

    def __repr__(self) -> str:
        return f"<Student {self.name}>"


class Module(Base):
    __tablename__ = 'module'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    students = relationship('Student', back_populates='modules', secondary=association_table)

    def __repr__(self) -> str:
        return f"<Module {self.name}>"


Base.metadata.create_all()


karl = Student(name='Karl')
eric = Student(name='Eric')
hanna = Student(name='Hanna')

maths = Module(name='Maths')
physics = Module(name='Physics')
chemistry = Module(name='Chemistry')

karl.modules.extend([maths, physics, chemistry])
eric.modules.extend([maths, physics])
hanna.modules.extend([maths, chemistry])

Session = sessionmaker(bind=engine)
session = Session()

session.add_all([karl, eric, hanna])

session.commit()

result = session.query(Module).all()

for module in result:
    print(f"{module} has {module.students}")
    for student in module.students:
        print(f"{student} has {student.modules}")
