#!/bin/bash

# ==============================
# CONFIGURACIÓN DEL SISTEMA
# ==============================
echo "🔹 Instalando dependencias del sistema..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nodejs npm mysql-server

# ==============================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ==============================
echo "🔹 Configurando MySQL..."
sudo systemctl start mysql
sudo systemctl enable mysql

MYSQL_USER="admin"
MYSQL_PASSWORD="admin"
MYSQL_DATABASE="notes_db"

# Crear usuario y base de datos en MySQL
sudo mysql -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;"
sudo mysql -e "CREATE USER IF NOT EXISTS '$MYSQL_USER'@'localhost' IDENTIFIED BY '$MYSQL_PASSWORD';"
sudo mysql -e "GRANT ALL PRIVILEGES ON $MYSQL_DATABASE.* TO '$MYSQL_USER'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# ==============================
# CONFIGURACIÓN DEL BACKEND
# ==============================
echo "🔹 Configurando el backend..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Generar nueva migración inicial
alembic revision --autogenerate -m "Initial migration"

# Aplicar migrasiones
echo "🔹 Aplicando migraciones..."
alembic upgrade head


# Ejecutar backend
echo "🔹 Iniciando el backend..."
uvicorn backend.app.main:app --host 0.0.0.0 --reload &

# ==============================
# CONFIGURACIÓN DEL FRONTEND
# ==============================
echo "🔹 Configurando el frontend..."
cd frontend || exit
npm install

# Ejecutar frontend
echo "🔹 Iniciando el frontend..."
npm run dev -- --host 0.0.0.0
cd ..

# ==============================
# FINALIZADO
# ==============================
echo "✅ La aplicación está corriendo en:"
echo "🔹 Backend: http://localhost:8000"
echo "🔹 Frontend: http://localhost:5173"