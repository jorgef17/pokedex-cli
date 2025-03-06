from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.note import NoteCreate, NoteResponse, NoteUpdate
from backend.app.schemas.note import CategoryResponse, CategoryCreate
from backend.app.services.note_service import NoteService
from typing import List

router = APIRouter()

# --- Notas ---

@router.post("/notes", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    return NoteService.create_note(db, note)

@router.get("/notes/active", response_model=List[NoteResponse])
def get_active_notes(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return NoteService.get_active_notes(db, skip=skip, limit=limit)

@router.get("/notes/archived", response_model=List[NoteResponse])
def get_archived_notes(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return NoteService.get_archived_notes(db, skip=skip, limit=limit)

@router.get("/notes", response_model=List[NoteResponse])
async def get_notes(db: Session = Depends(get_db)):
    return NoteService.get_notes(db)

@router.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = NoteService.get_note(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return note

@router.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note_update: NoteUpdate, db: Session = Depends(get_db)):
    updated_note = NoteService.update_note(db, note_id, note_update)
    if updated_note is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return updated_note

@router.delete("/notes/{note_id}", response_model=dict)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    success = NoteService.delete_note(db, note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return {"message": "Nota eliminada exitosamente"}

@router.put("/notes/{note_id}/archive", response_model=NoteResponse)
def archive_note(note_id: int, db: Session = Depends(get_db)):
    note = NoteService.archive_note(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return note

@router.put("/notes/{note_id}/unarchive", response_model=NoteResponse)
def unarchive_note(note_id: int, db: Session = Depends(get_db)):
    note = NoteService.unarchive_note(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return note

# --- Categorías ---

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return NoteService.get_categories(db)

@router.post("/categories", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return NoteService.create_category(db, category)

@router.post("/notes/{note_id}/categories/{category_id}", response_model=NoteResponse)
def add_category_to_note(note_id: int, category_id: int, db: Session = Depends(get_db)):
    note = NoteService.add_category_to_note(db, note_id, category_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Nota o categoría no encontrada")
    return note

@router.delete("/notes/{note_id}/categories/{category_id}", response_model=NoteResponse)
def remove_category_from_note(note_id: int, category_id: int, db: Session = Depends(get_db)):
    note = NoteService.remove_category_from_note(db, note_id, category_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Nota o categoría no encontrada")
    return note


@router.get("/categories/{category_id}/notes", response_model=List[NoteResponse])
def get_notes_by_category(category_id: int, db: Session = Depends(get_db)):
    return NoteService.get_notes_by_category(db, category_id)

@router.delete("/categories/{category_id}", response_model=dict)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    success = NoteService.delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Categoría no encontrada o en uso")
    return {"message": "Categoría eliminada exitosamente"}
