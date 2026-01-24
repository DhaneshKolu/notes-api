from passlib.context import CryptContext
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta,timezone
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)



from app.database import get_db
from app import models


pwd_context = CryptContext(schemes=["argon2"],deprecated = "auto")

oauth_scheme  = OAuth2PasswordBearer(tokenUrl="/users/login")

def hashed_password(password : str)->str:
    return pwd_context.hash(password)

def verify_password(plain,hashed):
    return pwd_context.verify(plain,hashed)

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    jwt_encoded = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return jwt_encoded

def get_current_user(token:str = Depends(oauth_scheme),db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.id==user_id).first()
    if user is None:
        raise credentials_exception
    
    return user




