from typing import List

from sqlalchemy import create_engine
from sqlalchemy import Column 
from sqlalchemy import String 
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import exc
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy import select


class Base(DeclarativeBase):
    pass


class Child(Base):
    __tablename__ = 'childrens'

    id = Column(Integer, primary_key=True)
    id : Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    name : Mapped[str] = mapped_column(String)
    age : Mapped[str] = mapped_column(String)


class User(Base):
    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(primary_key=True)
    firstname : Mapped[str] = mapped_column(String)
    telephone_number : Mapped[str] = mapped_column(String)
    email : Mapped[str] = mapped_column(String)
    password : Mapped[str] = mapped_column(String)
    role : Mapped[str] = mapped_column(String)
    created_at : Mapped[str] = mapped_column(String)
    children : Mapped[List["Child"]] = relationship('Child', backref='user')


    def __init__(self, data):
        self.firstname = data.get('firstname')
        self.telephone_number = data.get('telephone_number')
        self.email = data.get('email')
        self.password = data.get('password')
        self.role = data.get('role')
        self.created_at = data.get('created_at')

        children = []
        for child_data in data.get('children', []):
            child = Child(name=child_data.get('name'), 
                          age=child_data.get('age'))
            children.append(child)
        self.children = children


engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def create_database(data):
    
    try:
        for item in data:
            user = User(item)
            session.add(user)
        session.commit()
        return 'Database Created'
    
    except exc.SQLAlchemyError as error:
        session.rollback()
        return f'Cannot create database: {error}'
    
    finally:
         session.close()



