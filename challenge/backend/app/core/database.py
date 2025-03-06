from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Dependencias para obtener una sesión en cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

