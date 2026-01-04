from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List

from app import models
from app.database import get_db
from app.auth import get_current_user
from app import schemas

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)
@router.post("/",response_model=schemas.NoteOut)
def create_note(
    note:schemas.CreateNote,
    db : Session = Depends(get_db),
    current_user =  Depends(get_current_user)
):
    new_note = models.Note(
        title = note.title,
        content = note.content,
        owner_id = current_user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("/",response_model=List[schemas.NoteOut])
def get_notes(
    db :Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(models.Note).filter(models.Note.owner_id==current_user.id,models.Note.is_archived==False).all()

@router.get("/archived",response_model= List[schemas.NoteOut])
def archived(
    db:Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return db.query(models.Note).filter(models.User.owner_id==user.id,models.Note.is_archived==True).all()
@router.patch("/{note_id}",response_model = schemas.NoteOut)

def update_note(
    note_id:int,
    note_update:schemas.NoteUpdate,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    note = db.query(models.Note).filter(models.Note.id==note_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "No note found")
    if note.owner_id!= current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = "Not authorised to update this note"
        )
    if note_update.title is not None:
        note.title = note_update.title
    if note_update.content is not None:
        note.content = note_update.content

    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}",status_code=status.HTTP_204_NO_CONTENT)

def note_delete(
    note_id:int,
    db : Session =Depends(get_db),
    current = Depends(get_current_user)
):
    note = db.query(models.Note).filter(models.Note.id==note_id).first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No note was found"
        )

    if note.owner_id!=current.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = "Not authorized to update the note"
        )
    
    note.is_archived = True
    db.commit()

@router.post("/{note_id}/restore",response_model = schemas.NoteOut)
def restore_note(
    note_id:int,
    db : Session = Depends(get_db),
    user = Depends(get_current_user)
):
    note = db.query(models.Note).filter(models.Note.id==note_id).first()
    if not note:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "Note could'nt be found"
        )
    if note.owner_id != user.id:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail = "Not Authorised"
        )
    
    note.is_archived = False
    db.commit()
    db.refresh(note)
    return note
    