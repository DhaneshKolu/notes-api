from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import json
import logging,time
from app import models, schemas
from app.database import get_db
from app.auth import get_current_user
from app.cache import redis_client
from fastapi import BackgroundTasks

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


def invalidate_notes_cache(user_id: int):
    if not redis_client:
        return

    try:
        keys = redis_client.keys(f"notes:{user_id}:*")
        for key in keys:
            redis_client.delete(key)
    except Exception:
        pass



@router.post("/", response_model=schemas.NoteOut)
def create_note(
    note: schemas.CreateNote,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    new_note = models.Note(
        title=note.title,
        content=note.content,
        owner_id=current_user.id,
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    invalidate_notes_cache(current_user.id)

    return new_note


@router.get("/", response_model=List[schemas.NoteOut])
def get_notes(
    limit: int = Query(10, ge=1, le=50),
    skip: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    cache_key = f"notes:{current_user.id}"

    if redis_client:
        try:
            cached_notes = redis_client.get(cache_key)
            if cached_notes:
                return json.loads(cached_notes)
        except Exception:
            pass

    notes = (
        db.query(models.Note)
        .filter(
            models.Note.owner_id == current_user.id,
            models.Note.is_archived.is_(False),
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    serialized_notes = [
        schemas.NoteOut.model_validate(note).model_dump()
        for note in notes
    ]

    if redis_client:
        try:
            redis_client.set(cache_key, json.dumps(notes), ex=300)
        except Exception:
            pass


    return serialized_notes


@router.get("/archived", response_model=List[schemas.NoteOut])
def get_archived_notes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return (
        db.query(models.Note)
        .filter(
            models.Note.owner_id == current_user.id,
            models.Note.is_archived.is_(True),
        )
        .all()
    )


@router.patch("/{note_id}", response_model=schemas.NoteOut)
def update_note(
    note_id: int,
    note_update: schemas.NoteUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    note = (
        db.query(models.Note)
        .filter(
            models.Note.id == note_id,
            models.Note.owner_id == current_user.id,
        )
        .first()
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No note found",
        )

    if note_update.title is not None:
        note.title = note_update.title
    if note_update.content is not None:
        note.content = note_update.content

    db.commit()
    db.refresh(note)

    invalidate_notes_cache(current_user.id)

    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    background_tasks : BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    note = (
        db.query(models.Note)
        .filter(
            models.Note.id == note_id,
            models.Note.owner_id == current_user.id,
        )
        .first()
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No note found",
        )

    note.is_archived = True
    db.commit()
    background_tasks.add_task(
        log_note_deletion,
        note_id,
        current_user.id,
    )


    invalidate_notes_cache(current_user.id)

    return None


@router.post("/{note_id}/restore", response_model=schemas.NoteOut)
def restore_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    note = (
        db.query(models.Note)
        .filter(
            models.Note.id == note_id,
            models.Note.owner_id == current_user.id,
        )
        .first()
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note could not be found",
        )

    note.is_archived = False
    db.commit()
    db.refresh(note)

    invalidate_notes_cache(current_user.id)

    return note


logger = logging.getLogger(__name__)

def log_note_deletion(note_id: int, user_id: int):
    time.sleep(1)  # simulate slow work
    logger.info(
        "Background task: Note %s deleted by user %s",
        note_id,
        user_id,
    )
