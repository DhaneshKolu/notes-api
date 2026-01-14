from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email:str
    password :str

class UserOut(BaseModel):
    id:int
    email:str

    class config:
        from_attributes = True

class CreateNote(BaseModel):
    title:str
    content:Optional[str]=None
    
from pydantic import BaseModel, ConfigDict
from typing import Optional

class NoteOut(BaseModel):
    id: int
    title: str
    content: Optional[str]
    is_archived: bool

    model_config = ConfigDict(from_attributes=True)


class NoteUpdate(BaseModel):
    title : Optional[str] = None
    content : Optional[str] = None

