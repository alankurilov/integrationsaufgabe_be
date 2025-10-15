from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped

class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key = True, index = True)
    firstName: Mapped[str] =  mapped_column(String(100)) 
    lastName: Mapped[str] =  mapped_column(String(100)) 
    email: Mapped[str] =  mapped_column(String(100)) 
    password: Mapped[str] =  mapped_column(String(100)) 
    
    given_votes: Mapped[list["Vote"]] = relationship(back_populates="voter", foreign_keys="Vote.voterID")
    received_votes: Mapped[list["Vote"]] = relationship(back_populates="choice", foreign_keys="Vote.choiceID")

class Vote(Base):
    __tablename__ = "votes"

    id: Mapped[int] = mapped_column(primary_key = True, index = True)
    voterID: Mapped[int] = mapped_column(ForeignKey("people.id")) 
    choiceID: Mapped[int] = mapped_column(ForeignKey("people.id")) 
    voter: Mapped["Person"] = relationship(back_populates = "given_votes", foreign_keys=[voterID])
    choice: Mapped["Person"] = relationship(back_populates = "received_votes", foreign_keys=[choiceID])