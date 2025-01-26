from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from flask import request
from app.models import User  # Asegúrate de que el modelo User esté importado

auth_ns = Namespace('auth', description='Autenticación')

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='Nombre de usuario'),
    'password': fields.String(required=True, description='Contraseña')
})

from flask_jwt_extended import create_access_token

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """Autenticar usuario"""
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # Verificar si el usuario existe y si la contraseña es correcta
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):  # Asumiendo que tienes un método `verify_password`
            # Crear el token, pasando el id del usuario como 'identity'
            token = create_access_token(identity=str(user.id))  # Convertimos user.id a string
            return {'access_token': token}, 200
        return {'error': 'Credenciales inválidas'}, 401
