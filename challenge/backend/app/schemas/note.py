from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str
    
class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    categories: Optional[List[int]] = []  # Permite agregar categorías al crear una nota

class NoteUpdate(NoteBase):
    title: Optional[str] = None
    content: Optional[str] = None
    categories: Optional[List[int]] = None  # Permite modificar las categorías

class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    is_archived: bool
    categories: List[CategoryResponse] = []  # Muestra las categorías asociadas

    class Config:
        from_attributes = True
