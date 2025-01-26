from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash
from app.models import User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import abort

# Lógica de autorización para solo administradores
def admin_required(fn):
    """Verifica que el usuario tenga el rol de administrador."""
    def wrapper(self, *args, **kwargs):  # Asegúrate de pasar "self" como primer argumento
        user_id = get_jwt_identity()  # Obtiene el ID del usuario desde el JWT
        
        if not user_id:
            abort(401, description="No se pudo obtener la identidad del usuario.")
        
        user = User.query.get(user_id)  # Busca al usuario en la base de datos
        
        if not user:
            abort(404, description="Usuario no encontrado.")
        
        if user.role and user.role.name != 'admin':  # Verifica si el usuario tiene rol 'admin'
            abort(403, description="No tienes permiso para realizar esta acción.")
        
        return fn(self, *args, **kwargs)  # Ejecuta la función si el usuario es admin
    return wrapper


# Definir el namespace
user_ns = Namespace('users', description='Operaciones relacionadas con usuarios')

# Modelo para validar datos de entrada y respuesta
user_model = user_ns.model('User', {
    'id': fields.Integer(readOnly=True, description='ID del usuario'),
    'username': fields.String(required=True, description='Nombre del usuario'),
    'email': fields.String(required=True, description='Correo electrónico del usuario'),
    'password': fields.String(required=True, description='Contraseña del usuario')
})

@user_ns.route('/')
class UserList(Resource):
    @jwt_required()  # Solo usuarios autenticados pueden listar usuarios
    @user_ns.marshal_list_with(user_model)
    def get(self):
        """
        Obtener todos los usuarios.
        Este método devuelve una lista de todos los usuarios registrados en el sistema.
        """
        users = User.query.all()
        return users

    @jwt_required()  # Solo usuarios autenticados pueden crear usuarios
    @user_ns.expect(user_model)
    def post(self):
        """
        Crear un nuevo usuario.
        Este método permite crear un nuevo usuario proporcionando nombre de usuario,
        correo electrónico y contraseña.
        """
        data = user_ns.payload
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Validar si el usuario o el email ya existen
        if User.query.filter_by(username=username).first():
            return {'error': 'El usuario ya existe'}, 400

        if User.query.filter_by(email=email).first():
            return {'error': 'El correo electrónico ya está registrado'}, 400

        # Hash de la contraseña
        hashed_password = generate_password_hash(password)

        # Crear nuevo usuario con los datos proporcionados
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': f'Usuario {username} creado con éxito'}, 201

@user_ns.route('/<int:user_id>')
@user_ns.param('user_id', 'El ID del usuario')
class UserDetail(Resource):
    @jwt_required()  # Solo usuarios autenticados pueden eliminar o actualizar
    @admin_required  # Solo administradores pueden eliminar o actualizar usuarios
    def delete(self, user_id):
        """
        Eliminar un usuario por ID.
        Este método elimina un usuario del sistema dado su ID. Solo un administrador puede realizar esta acción.
        """
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': f'Usuario {user.username} eliminado con éxito'}, 200

    @jwt_required()  # Solo usuarios autenticados pueden eliminar o actualizar
    @admin_required  # Solo administradores pueden eliminar o actualizar usuarios
    @user_ns.expect(user_model)
    def put(self, user_id):
        """
        Actualizar un usuario por ID.
        Este método permite actualizar los datos de un usuario dado su ID. Solo un administrador puede realizar esta acción.
        """
        data = user_ns.payload
        user = User.query.get_or_404(user_id)

        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)

        password = data.get('password')
        if password:
            # Si se proporciona una nueva contraseña, la actualizamos
            hashed_password = generate_password_hash(password)
            user.password = hashed_password

        db.session.commit()
        return {'message': f'Usuario {user.username} actualizado con éxito'}, 200
