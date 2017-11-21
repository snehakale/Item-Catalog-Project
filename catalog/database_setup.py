''' This is database_setup.py python program.
    It holds the classes definitions
    representing tables in given database.'''

# Importing sqlalchemy modules to create tables
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# base object
Base = declarative_base()


# class User for user table data
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


# class DanceSchool for danceschool table data
class DanceSchool(Base):
    __tablename__ = 'danceschool'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    address = Column(String(250))
    # Foreign key for user table
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    # Cascade relationship for delete operation
    danceclass = relationship('DanceClass', cascade='all, delete-orphan')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name' : self.name,
            'id' : self.id,
            'address' : self.address,
        }


# class DanceClass for danceclass table data
class DanceClass(Base):
    __tablename__ = 'danceclass'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    teacher = Column(String(250))
    sessions = Column(String(100))
    fees = Column(String(100))
    # Foreign key for user table
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    # Foreign key for danceSchool table
    dance_school_id = Column(Integer, ForeignKey('danceschool.id'))
    danceschool = relationship(DanceSchool)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name' : self.name,
            'id' : self.id,
            'description' : self.description,
            'teacher' : self.teacher,
            'sessions' : self.sessions,
            'fees' : self.fees,
           }

# DB Engine
engine = create_engine('sqlite:///dancedataapp.db')

Base.metadata.create_all(engine)
