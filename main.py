# main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import UUID
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Person(BaseModel):
    firstName: str = Field(min_length = 1)
    lastName: str = Field(min_length = 1, max_length = 99)
    email: str = Field(min_length = 1, max_length = 99)
    password: str = Field(min_length = 1, max_length = 99)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL Vue сервера
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/login")
def log_in(person: Person, db: Session = Depends(get_db)): 
    person_check = db.query(models.Person).filter(models.Person.email == person.email).first()
    if(person_check.password == person.password):
        return person.email
 
    raise HTTPException(
        status_code = 404,
        detail=f"password is wrong"
    )


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Person).all()

@app.post("/")
def create_person(person: Person, db: Session = Depends(get_db)):
    person_check = db.query(models.Person).filter(models.Person.email == person.email).first()
    if person_check is None:        
        person_model = models.Person()
        person_model.firstName = person.firstName
        person_model.lastName = person.lastName
        person_model.email = person.email
        person_model.password = person.password

        db.add(person_model)
        db.commit()
    
        return person
    
    raise HTTPException(
        status_code = 400,
        detail=f"user {person.email} already exists"
    )

@app.put("/{person_id}")
def update_person(person_id: int, person: Person, db: Session = Depends(get_db)):
    person_model = db.query(models.Person).filter(models.Person.id == person_id).first()

    if person_model is None:
        raise HTTPException(
            status_code = 404,
            detail=f"ID {person_id}: does not exist"
        )
    person_model.firstName = person.firstName
    person_model.lastName = person.lastName
    person_model.email = person.email
    person_model.password = person.password

    db.add(person_model)
    db.commit()

    return person

@app.delete("/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    person_model = db.query(models.Person).filter(models.Person.id == person_id).first()

    if person_model is None:
        raise HTTPException(
            status_code = 404,
            detail=f"ID {person_id}: does not exist"
        )
    db.query(models.Person).filter(models.Person.id == person_id).delete()

    db.commit()