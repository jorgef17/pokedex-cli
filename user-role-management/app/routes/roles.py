from flask_restx import Namespace, Resource, fields
from app.models import Role, User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import abort

# Lógica de autorización para solo administradores
def admin_required(fn):
    """Verifica que el usuario tenga el rol de administrador."""
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()  # Obtiene el ID del usuario desde el JWT
        
        if not user_id:
            abort(401, description="No se pudo obtener la identidad del usuario.")
        
        user = User.query.get(user_id)  # Busca al usuario en la base de datos
        
        if not user:
            abort(404, description="Usuario no encontrado.")
        
        if user.role and user.role.name != 'admin':  # Verifica si el usuario tiene rol 'admin'
            abort(403, description="No tienes permiso para realizar esta acción.")
        
        return fn(*args, **kwargs)  # Ejecuta la función si el usuario es admin
    return wrapper


# Definir el namespace
role_ns = Namespace('roles', description='Operaciones relacionadas con roles')

# Modelo para validar datos de entrada y respuesta
role_model = role_ns.model('Role', {
    'id': fields.Integer(readOnly=True, description='ID del rol'),
    'name': fields.String(required=True, description='Nombre del rol')
})

assign_role_model = role_ns.model('AssignRole', {
    'user_id': fields.Integer(required=True, description='ID del usuario'),
    'role_id': fields.Integer(required=True, description='ID del rol')
})

@role_ns.route('/')
class RoleList(Resource):
    @jwt_required()  # Solo usuarios autenticados pueden listar roles
    @role_ns.marshal_list_with(role_model)
    def get(self):
        """Obtener todos los roles"""
        roles = Role.query.all()
        return roles

    @jwt_required()  # Solo usuarios autenticados pueden crear roles
    @role_ns.expect(role_model)
    def post(self):
        """Crear un nuevo rol"""
        data = role_ns.payload
        name = data.get('name')

        if Role.query.filter_by(name=name).first():
            return {'error': 'El rol ya existe'}, 400

        new_role = Role(name=name)
        db.session.add(new_role)
        db.session.commit()
        return {'message': f'Rol {name} creado con éxito'}, 201

@role_ns.route('/<int:role_id>')
@role_ns.param('role_id', 'El ID del rol')
class RoleDetail(Resource):
    @jwt_required()  # Solo usuarios autenticados pueden eliminar o actualizar
    @admin_required  # Solo administradores pueden eliminar o actualizar roles
    def delete(self, role_id):
        """Eliminar un rol por ID"""
        role = Role.query.get_or_404(role_id)
        db.session.delete(role)
        db.session.commit()
        return {'message': f'Rol {role.name} eliminado con éxito'}, 200

    @jwt_required()  # Solo usuarios autenticados pueden eliminar o actualizar
    @admin_required  # Solo administradores pueden eliminar o actualizar roles
    @role_ns.expect(role_model)
    def put(self, role_id):
        """Actualizar un rol por ID"""
        data = role_ns.payload
        role = Role.query.get_or_404(role_id)

        role.name = data.get('name', role.name)
        db.session.commit()
        return {'message': f'Rol {role.name} actualizado con éxito'}, 200

@role_ns.route('/assign-role')
class AssignRole(Resource):
    @jwt_required()  # Solo usuarios autenticados pueden asignar roles
    @role_ns.expect(assign_role_model)  # Espera los parámetros user_id y role_id en el cuerpo de la solicitud
    def post(self):
        """Asignar un rol a un usuario"""
        data = role_ns.payload
        user_id = data.get('user_id')  # ID del usuario al que se asignará el rol
        role_id = data.get('role_id')  # ID del rol que se asignará

        # Obtener el usuario y el rol de la base de datos
        user = User.query.get(user_id)
        role = Role.query.get(role_id)

        if not user:
            return {'error': 'Usuario no encontrado'}, 404
        if not role:
            return {'error': 'Rol no encontrado'}, 404

        # Verificar si el usuario ya tiene el rol asignado
        if user.role and user.role.id == role.id:  # Se asegura de que user.role no sea None
            return {'message': 'El usuario ya tiene este rol asignado'}, 200

        # Asignar el rol al usuario
        user.role = role
        db.session.commit()

        return {'message': f'Rol {role.name} asignado al usuario {user.username} con éxito'}, 200
