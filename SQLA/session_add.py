from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, create_engine

engine = create_engine('postgresql+psycopg2://deniz@localhost:54321/sqla', echo=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

class Language(Base):
    __tablename__ = 'language'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)

Base.metadata.create_all()

german = Language(name='Germann')
english = Language(name='English')
italian = Language(name='Italian')

session.add_all([
    german, english, italian
])

session.commit()

session2 = Session()

germann = session2.query(Language).filter(Language.name.ilike('germann')).scalar()
germann.name = 'German'

session2.commit()