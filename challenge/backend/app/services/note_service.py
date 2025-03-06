from sqlalchemy.orm import Session
from backend.app.models.note import Note, Category
from backend.app.schemas.note import NoteCreate, NoteUpdate, CategoryCreate

class NoteService:
    @staticmethod
    def create_note(db: Session, note: NoteCreate):
        """Crea una nueva nota en la base de datos con categorías opcionales."""
        db_note = Note(title=note.title, content=note.content)
        db.add(db_note)
        db.commit()
        db.refresh(db_note)

        # Asociar categorías si se proporcionan
        if note.categories:
            for category_id in note.categories:
                category = db.query(Category).filter(Category.id == category_id).first()
                if category and category not in db_note.categories:
                    db_note.categories.append(category)

            db.commit()
            db.refresh(db_note)

        return db_note

    @staticmethod
    def get_notes(db: Session, skip: int = 0, limit: int = 10):
        """Obtiene una lista de notas con sus categorías."""
        return db.query(Note).offset(skip).limit(limit).all()

    @staticmethod
    def get_note(db: Session, note_id: int):
        """Obtiene una nota por su ID con sus categorías."""
        return db.query(Note).filter(Note.id == note_id).first()

    @staticmethod
    def update_note(db: Session, note_id: int, note_update: NoteUpdate):
        """Actualiza una nota existente y sus categorías."""
        db_note = db.query(Note).filter(Note.id == note_id).first()
        if not db_note:
            return None

        if note_update.title is not None:
            db_note.title = note_update.title
        if note_update.content is not None:
            db_note.content = note_update.content

        db.commit()
        db.refresh(db_note)
        return db_note

    @staticmethod
    def delete_note(db: Session, note_id: int):
        """Elimina una nota por su ID."""
        db_note = db.query(Note).filter(Note.id == note_id).first()
        if db_note:
            db.delete(db_note)
            db.commit()
            return True
        return False

    @staticmethod
    def archive_note(db: Session, note_id: int):
        """Archiva una nota por su ID."""
        db_note = db.query(Note).filter(Note.id == note_id).first()
        if db_note:
            db_note.is_archived = True
            db.commit()
            db.refresh(db_note)
            return db_note
        return None

    @staticmethod
    def unarchive_note(db: Session, note_id: int):
        """Desarchiva una nota por su ID."""
        db_note = db.query(Note).filter(Note.id == note_id).first()
        if db_note:
            db_note.is_archived = False
            db.commit()
            db.refresh(db_note)
            return db_note
        return None

    @staticmethod
    def get_active_notes(db: Session, skip: int = 0, limit: int = 10):
        """Obtiene una lista de notas activas (no archivadas)."""
        return db.query(Note).filter(Note.is_archived == False).all()

    @staticmethod
    def get_archived_notes(db: Session, skip: int = 0, limit: int = 10):
        """Obtiene una lista de notas archivadas."""
        return db.query(Note).filter(Note.is_archived == True).all()

    # --- Categorías ---

    @staticmethod
    def get_categories(db: Session):
        """Obtiene todas las categorías disponibles."""
        return db.query(Category).all()

    @staticmethod
    def add_category_to_note(db: Session, note_id: int, category_id: int):
        """Agrega una categoría a una nota."""
        db_note = db.query(Note).filter(Note.id == note_id).first()
        db_category = db.query(Category).filter(Category.id == category_id).first()

        if not db_note or not db_category:
            return None

        if db_category not in db_note.categories:  # Evitar duplicados
            db_note.categories.append(db_category)
            db.commit()
            db.refresh(db_note)

        return db_note

    @staticmethod
    def remove_category_from_note(db: Session, note_id: int, category_id: int):
        """Elimina una categoría de una nota."""
        db_note = db.query(Note).filter(Note.id == note_id).first()
        db_category = db.query(Category).filter(Category.id == category_id).first()

        if not db_note or not db_category:
            return None

        if db_category in db_note.categories:
            db_note.categories.remove(db_category)
            db.commit()
            db.refresh(db_note)

        return db_note

    @staticmethod
    def create_category(db: Session, category_data: CategoryCreate):
        new_category = Category(name=category_data.name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    
    @staticmethod
    def get_notes_by_category(db: Session, category_id: int):
        return db.query(Note).join(Note.categories).filter(Category.id == category_id).all()

    @staticmethod
    def delete_category(db: Session, category_id: int):
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            return False
        
        # Verificar si la categoría está asignada a alguna nota
        if category.notes:
            return False
        
        db.delete(category)
        db.commit()
        return True
