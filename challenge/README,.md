# **Notes application with FastAPI and React**

## **Descripción**
This project is a notes application that allows creating, editing, deleting and archiving notes. The API is developed in **FastAPI**, using **SQLAlchemy** and **Alembic** to handle the database. The frontend is a **SPA (Single Page Application)** created with **React and Vite**.

## **Description**
List of required tools with their exact versions:

- **Python 3.12**
- **Node.js 18.17**
- **npm 9.6.7**
- **MySQL 8.0**
- **Alembic 1.13**
- **FastAPI 0.110**
- **SQLAlchemy 2.0**
- **React 18**
- **Vite 6.2.0**

## **Installation and Configuration**
The system includes an `start.sh` script that automates the whole process. By executing it, it takes care of:

1. **Configure the backend:**
   - Create and activate a Python virtual environment.
   - Install dependencies from `requirements.txt`.
   - Configure the database in MySQL.
   - Generate and apply migrations with Alembic.

2. **Configure the frontend:**
   - Install the dependencies with `npm install`.
   - Start the development server.

### **Running the application**
To start the whole system, it is only necessary to run:

```sh
chmod +x start.sh
./start.sh
```

This command will run the backend and frontend automatically.

## **Manual Execution (Optional)**
If you prefer to do it manually, follow these steps:

### **Backend**
```sh
python -m venv venv
source venv/bin/activate  #  Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn backend.app.main:app --host 0.0.0.0 --reload &
```

### **Frontend**
```sh
cd frontend
npm install
npm run dev
```

## **Usage**
- The API will be available at: **`http://localhost:8000`**
- The frontend application will be at: **`http://localhost:5173`**
- The API documentation can be found at: **`http://localhost:8000/docs`**

## **Database**
MySQL is used, and the database is called `notes_db`.  
The migration system with Alembic automatically manages the database structur

## **Main endpoints**
Some of the main API endpoints:

### **Notes**

- `GET /notes` → Get all notes.
- `POST /notes` → Create a new note.
- `GET /notes/active` → Get active notes.
- `GET /notes/archived` → Get archived notes.
- `GET /notes/{note_id}` → Get a specific note.
- `PUT /notes/{note_id}` → Update a note.
- `DELETE /notes/{note_id}` → Delete a note.
- `PUT /notes/{note_id}/archive` → Archive a note.
- `PUT /notes/{note_id}/unarchive` → Unarchive a note.

### **Categories**

- `GET /categories` → Get all categories.
- `POST /categories` → Create a category.
- `DELETE /categories/{category_id}` → Delete a category.
- `GET /categories/{category_id}/notes` → Get notes by category.

### **Note-Category Association**

- `POST /notes/{note_id}/categories/{category_id}` → Add a category to a note.
- `DELETE /notes/{note_id}/categories/{category_id}` → Remove a category from a note.



## **Autor**
Developed by Jorge Fontalvo Bonett.  
