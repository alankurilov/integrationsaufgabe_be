from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Person 
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = '42acd4754321f76d9fd75df2016f883d'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['argon2']) # Change to argon_context
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    person_check = db.query(Person).filter(Person.email == create_user_request.email).first()
    if person_check is None: 
        create_user_model = Person(
            email=create_user_request.email,
            password=bcrypt_context.hash(create_user_request.password),
            firstName=create_user_request.first_name,
            lastName=create_user_request.last_name,
        ) 
        db.add(create_user_model)
        db.commit()
        return create_user_request
    raise HTTPException(
        status_code = 400,
        detail=f"user {create_user_request.email} already exists"
    )



@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user:Person = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    token = create_access_token(user.email, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}

def authenticate_user(username: str, password: str, db):
    user = db.query(Person).filter(Person.email == username).first()
    print(user.password)
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)