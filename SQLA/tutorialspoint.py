"""
LEARNINGS

the metadata object holds all tables and related views through binding to a database-engine
a sql expression needs to defined and then executed
sql-methods and functions use values directly to manipulate the sql statements
textual sql can be used with bound parameters
an alias can be used to rename a table temporarily for a queue
"""
from operator import and_
from sqlalchemy import bindparam, create_engine

engine = create_engine("postgresql+psycopg2://deniz:@localhost:54321/sqla", echo=True)


# CREATING TABLE
from sqlalchemy import \
    MetaData, Table, Column, Integer, String


meta = MetaData(engine)

students = Table(
    'students', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('lastname', String)
)


#SQL EXPRESSIONS
meta.create_all()  # DOES NOT RE-INIT THE DB
ins = students.insert().values(name="Denix")  # DOES NOTHING ATM
print(students.delete())
print(students.update())
engine.execute("INSERT INTO students(name) VALUES('deniz')")  # EXECUTES PROPERLY


# EXECUTING EXPRESSION
conn = engine.connect()
ins = students.insert().values(name="Deniz", lastname="Grollmusz")  # DECLARATION OF AN EXPRESSION WITHOUT EXECUTION
result = conn.execute(ins)  # EXPRESSIONS NEED TO BE EXECUTED
print(result.inserted_primary_key)
conn.execute(students.insert(), [
    {'name': 'lucas', 'lastname': 'bek'},
    {'name': 'phil', 'lastname': 'bosche'},
    {'name': 'timbo', 'lastname': '???'},
    {'name': 'pauly', 'lastname': 'pauly'},
    {'name': 'sang', 'lastname': 'sensei'}
])


# SELECTING ROWS
s = students.select()  # SELECT * FROM STUDENTS
result = conn.execute(s)
row = result.fetchone()  # FETCHING INCREMENTS THE
row = result.fetchone()  # CURSOR'S INDEX
for row in result:
    print(row)
sw = students.select().where(students.c.id < 10)
result = conn.execute(sw)
for row in result:
    print(f"where + {row}")


# USING TEXTUAL SQL
from sqlalchemy import text
t = text("SELECT * FROM students WHERE name NOT ILIKE 'deNiz'")
result = conn.execute(t)
print(result.fetchall())

t2 = text("SELECT * FROM students WHERE name NOT BETWEEN :x AND :y")  # DEFINE BOUND PARAMETERS
result = conn.execute(t2, x="c", y="e")  # INSERT VALUES AS BOUND PARAMETERS
print(result.fetchall())

stmt = text("SELECT * FROM students WHERE id BETWEEN :x AND :y")
stmt = stmt.bindparams(  # EXPLICITLY TYPE THE BOUND PARAMETERS
    bindparam("x", type_= Integer),
    bindparam("y", type_= Integer)
)  
result = conn.execute(stmt, {"x":1, "y":11})
print(result.fetchall())

from sqlalchemy.sql import select
s = select([text("students.name, students.lastname, students.id FROM students")]).where(text('students.id < :x'))  # SELECT/WHERE EXPRESSION FILLED WITH TEXT
result = conn.execute(s, x=6)
print(result.fetchall())

from sqlalchemy import and_
s = select([text("students.name, students.lastname, students.id FROM students")]) \
    .where(
        and_(  # USE AND_ TO CONCATENATE EXPRESSIONS FOR ONE WHERE PREDICATE
            text("students.id < :x"),
            text("students.name NOT ILIKE :y")
        )
    )
result = conn.execute(s, x=50, y='deniz')
print(result.fetchall())


# USING ALIASES
from sqlalchemy.sql import alias
st = students.alias("studs")
s = select([st]).where(st.c.id < 15)
result = conn.execute(s)
print(result.fetchall())
