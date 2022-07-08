"""
LEARNINGS

the metadata object holds all tables and related views through binding to a database-engine
a sql statement needs to defined and then executed
sql-methods and functions use values directly to manipulate the sql statements
textual sql can be used with bound parameters
an alias can be used to rename a table temporarily for a query
EXPRESSION(TABLE) OVER TABLE.EXPRESSION()
inject values into a stmt with method-chaining or giving a list-argument to the conn.execute()-call
to join tables, add a list of tables to the select expression and define the column on which they are joined
"""
from sqlalchemy import ForeignKey, bindparam, create_engine

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
engine.execute("INSERT INTO students(name) VALUES('deniz')")  # EXECUTES THE STATEMENT


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
for row in result:  # LOOP THROUGH THE RESULTS' CURSOR AND PRINT EVERY ROW
    print(row)

sw = students.select().where(students.c.id < 10)  # CHAIN A WHERE EXPRESSION
result = conn.execute(sw)
for row in result:
    print(f"where + {row}")


# USING TEXTUAL SQL
from sqlalchemy import text
t = text("SELECT * FROM students WHERE name NOT ILIKE 'deNiz'")
result = conn.execute(t)
print(result.fetchall())

t2 = text("SELECT * FROM students WHERE name NOT BETWEEN :x AND :y")  # DEFINE BOUND PARAMETERS
result = conn.execute(t2, x="c", y="e")  # VALUES AS ARGUMENTS FOR BOUND PARAMETERS
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
from sqlalchemy.sql.expression import select
st = students.alias("studs")
s = select([st]).where(st.c.id < 15)
result = conn.execute(s)
print(result.fetchall())


# USING UPDATE EXPRESSION
stmt = students.update() \
    .where(students.c.name == 'deniz') \
    .where(students.c.lastname == None) \
    .values(lastname='Grollmusz')
conn.execute(stmt)

from sqlalchemy.sql.expression import update, select  # CLEANER TO DO SELECT(STUDENTS) THAN STUDENTS.SELECT()
stmt = update(students) \
    .where(students.c.lastname == 'Grollmusz') \
    .values(lastname='grollmusz')
conn.execute(stmt)
stmt = select(students)
print(conn.execute(stmt).fetchall())


# USING DELETE EXPRESSION
from sqlalchemy.sql.expression import delete
stmt = delete(students) \
    .where(students.c.id > 15)
conn.execute(stmt)
stmt = select(students)
print(conn.execute(stmt).fetchall())


# USING MULTIPLE TABLES
from sqlalchemy import ForeignKey
from sqlalchemy.sql.expression import insert

addresses = Table(
    'addresses', meta,
    Column('id', Integer, primary_key=True),
    Column('st_id', Integer, ForeignKey('students.id')),
    Column('postal_add', String),
    Column('email_add', String)
)

meta.create_all()

insert = insert(addresses).values([
    {'st_id': 1, 'postal_add': 'Berlin'},
    {'st_id': 10, 'postal_add': 'Raunheim'},
    {'st_id': 14, 'postal_add': 'Ruesselsheim'},
])
conn.execute(insert)
conn.execute(delete(addresses).where(addresses.c.id > 3))

select_stmt = select([students, addresses]).where(students.c.id == addresses.c.st_id)
print(conn.execute(select_stmt).fetchall())


# USING MUTLIPLE TABLE UPDATES
stmt = (
    update(students).
    where(students.c.id == addresses.c.id).
    values(lastname='The Great Family', postal_add='Ruesselsheim')
)
# conn.execute(stmt)  # DOES NOT WORK. SQLA DOESN'T SEE THAT POSTAL_ADD BELONGS TO ADDRESSES-TABLE


# PARAMETER ORDERED UPDATES
stmt = (
    addresses.update(preserve_parameter_order=True)
    .values([(addresses.c.postal_add, '20'), (addresses.c.email_add, addresses.c.postal_add + '10')])
)
conn.execute(stmt)

stmt = (
    addresses.update(preserve_parameter_order=True)
    .values([(addresses.c.email_add, addresses.c.postal_add + '10'), (addresses.c.postal_add, '20')])
)
conn.execute(stmt)