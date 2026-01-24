from sqlalchemy import Column,Integer,String,Boolean,Text,ForeignKey,DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__="users"

    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True,index =True,nullable = False)
    hashed_password = Column(String,nullable= False)

    notes = relationship("Note",back_populates = "owner")    


class Note(Base):
    __tablename__="notes"

    id = Column(Integer,primary_key = True,index=True)
    title = Column(String,nullable=False)
    content = Column(Text,nullable = False)
    is_archived = Column(Boolean,default = False)
    created_at = Column(DateTime(timezone=True),server_default = func.now(),nullable=False)
    updated_at = Column(DateTime(timezone = True),onupdate=func.now())

    owner_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    
    owner = relationship("User",back_populates="notes")


