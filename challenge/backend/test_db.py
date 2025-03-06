from app.core.database import engine
from sqlalchemy import text

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Conexión exitosa a la base de datos:", result.fetchone())
    except Exception as e:
        print("❌ Error al conectar a la base de datos:", e)

if __name__ == "__main__":
    test_connection()


