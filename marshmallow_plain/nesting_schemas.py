"""
LEARNINGS
to nest schemas, exclude attributes that backref to the origin-schema (recursion error!!)
"""


from datetime import datetime
from pprint import pprint
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import DateTime, create_engine, Column, String, Table, ForeignKey, Integer

engine = create_engine('postgresql+psycopg2://deniz@localhost:54321/sqla', echo=False)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine, expire_on_commit=True)

class User(Base):
    """
    name, email. 
    optional: employer, friends, blogs
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    employer = Column(String, default=None)
    blogs = relationship('Blog', back_populates='author')

class Blog(Base):
    """
    title
    optional: author
    """
    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey(column=User.id))
    author = relationship(User, back_populates='blogs')

Base.metadata.create_all()



from marshmallow import Schema, fields

class UserSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer()
    name = fields.String()
    email = fields.Email()
    created_at = fields.DateTime()
    blogs = fields.List(fields.Nested('BlogSchema', only=('id','title','author')))

class BlogSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    author = fields.Pluck(UserSchema, 'name')

freddy = User(name='Freddy', email='Freddy@beach.org')
volleyblog = Blog(title='Volleyball Blog', author=freddy)
physicsblog = Blog(title='Physics Blog', author=freddy)


session = Session()
session.add(freddy)
session.commit()

freddy_serialized = UserSchema().dump(obj=freddy)
pprint(freddy_serialized, indent=2)