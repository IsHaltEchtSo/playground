from sqlalchemy import create_engine
from sqlalchemy.sql.expression import select
from tutorialspoint_core import students, addresses

engine = create_engine('postgresql+psycopg2://deniz@localhost:54321/sqla')

conn = engine.connect()

s_stmt = select([addresses, students]).where(addresses.c.st_id == students.c.id)

print(conn.execute(s_stmt).fetchall())