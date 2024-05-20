from typing import List

from fastapi import FastAPI, APIRouter
from sqlalchemy import desc
from starlette import status
import models
import schemas
from database import engine, get_db
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models import Note

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


router = APIRouter(
    prefix='/notes',
)


@app.get('/')
def get_routes():
    return ['/notes', '/notes/<pk>']


@app.get('/notes')
async def get_notes(db: Session = Depends(get_db)):
    notes_objects = db.query(Note).order_by(desc(Note.timestamp)).all()
    return notes_objects

@app.get('/notes/<pk>', response_model=schemas.NoteBase)
def get_note(pk: int, db: Session = Depends(get_db)):
    note_object = db.query(Note).filter(Note.id==pk).first()
    if note_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')
    return note_object


@app.post('/notes', status_code=status.HTTP_201_CREATED, response_model=schemas.NoteCreate)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    note_object = Note(**note.dict())
    db.add(note_object)
    db.commit()
    db.refresh(note_object)
    return note_object


@app.put('/notes/{pk}', response_model=schemas.NoteBase)
def update_note(pk: int, note: schemas.NoteBase, db: Session = Depends(get_db)):
    note_object = db.query(Note).get(pk)
    if note_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')

        # Update the attributes of the note_object
    note_object.title = note.title
    note_object.text = note.text

    db.commit()

    return note_object


@app.delete('/notes/<pk>', status_code=status.HTTP_204_NO_CONTENT)
def delete_note(pk: int, db: Session = Depends(get_db)):

    note_object = db.query(Note).filter(Note.id == pk).first()

    if note_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')

    db.delete(note_object)
    db.commit()
    return {'message': 'Note deleted'}
