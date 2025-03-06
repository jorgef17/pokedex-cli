from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import pytz

Base = declarative_base()

# Tabla intermedia para la relación muchos a muchos entre Notas y Categorías
note_categories = Table(
    "note_categories",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
)

# Zona horaria de Bogotá
bogota_tz = pytz.timezone("America/Bogota")

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(bogota_tz))
    is_archived = Column(Boolean, default=False)  

       # Relación con categorías
    categories = relationship("Category", secondary=note_categories, back_populates="notes")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False) 
    # Relación con notas
    notes = relationship("Note", secondary=note_categories, back_populates="categories")
