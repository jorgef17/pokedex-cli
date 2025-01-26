from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
api = Api(
    title="User-Role Management",
    version="1.0",
    description="API for managing users and roles"
)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['JWT_SECRET_KEY'] = 'myjwtsecret'  # Asegúrate de que la clave JWT esté configurada

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    # Registrar namespaces
    from .routes import user_ns, role_ns, auth_ns  # Asegúrate de importar auth_ns aquí
    api.add_namespace(user_ns, path='/users')
    api.add_namespace(role_ns, path='/roles')
    api.add_namespace(auth_ns, path='/auth')  # Registrar el namespace de autenticación

    return app
