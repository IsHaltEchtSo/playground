from venv import create
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('postgresql+psycopg2://deniz@localhost:54321/sqla', echo=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
