from fastapi import APIRouter,HTTPException,status,Depends
from app.database import get_db
from app import models
from app import schemas
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import hashed_password,verify_password,create_access_token

router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/",response_model = schemas.UserOut)

def register(user:schemas.UserCreate,db:Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400,detail = "Email already registered")
    new_user = models.User(
        email = user.email,
        hashed_password = hashed_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")

def login(
    form_data:OAuth2PasswordRequestForm = Depends(),
    db :Session = Depends(get_db)
):
    user =db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials")
    token = create_access_token({"user_id":user.id})
    return {"access_token":token,"token_type":"bearer"}