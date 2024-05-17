from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
print("Importing models...")
from models import User
print("Models imported successfully.")

from extensions import db

class Register(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400
        if not all(k in data for k in ("username", "password", "email")):
            return {'message': 'Missing data'}, 400
        
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        new_user = User(username=data['username'], password=hashed_password, email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400
        
        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return {'message': 'Invalid username or password'}, 401
        return {'message': 'Logged in successfully'}, 200

def initialize_routes(api):
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')
