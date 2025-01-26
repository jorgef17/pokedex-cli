from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='users')

    def verify_password(self, password):
        """Verificar si la contraseña proporcionada coincide con la almacenada"""
        return check_password_hash(self.password, password)

    @classmethod
    def hash_password(cls, password):
        """Generar un hash de la contraseña para almacenamiento"""
        return generate_password_hash(password)
