from sqlalchemy import Column, Integer, String
from database import Base

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key = True, index = True)
    firstName = Column(String) 
    lastName = Column(String)
    email = Column(String)
    password = Column(String)