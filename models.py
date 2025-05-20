from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key = True, index = True)
    firstName = Column(String) 
    lastName = Column(String)
    email = Column(String)
    password = Column(String)
    votes = relationship("Vote", back_populates="person")

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key = True, index = True)
    firstName = Column(String) 
    lastName = Column(String)
    votes = relationship("Vote", back_populates="candidate")

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key = True, index = True)
    personId = Column(Integer, ForeignKey("people.id")) 
    candidateId = Column(Integer, ForeignKey("candidates.id"))
    person = relationship("Person", back_populates="votes")
    candidate = relationship("Candidate", back_populates="votes")