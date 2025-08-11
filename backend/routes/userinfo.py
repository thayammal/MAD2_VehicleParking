# userinfo.py
from flask_restful import Resource
from flask import request, jsonify, make_response
from models import db, User, ParkingLot, Reservation
from flask_security import current_user
from datetime import datetime

#Admin need to get all user info
class UserInfoResource(Resource):
    def get(self):
        users = User.query.all()
        if not users:
            return make_response(jsonify({'status': 'error', 'message': 'No users found'}), 404)
        
        user_list = []
        for user in users:
            if user.username != 'admin':
                user_list.append({
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'address': user.address,
                'phone_number': user.phone_number,
                'last_login_at': user.last_login_at.isoformat() if user.last_login_at else None,
                'roles': [role.name for role in user.roles],
            })
        return make_response(jsonify({'status': 'ok', 'users': user_list}), 200)

    def post(self):
        data = request.get_json()
        print('the frontend data',data)
        try:
            new_user = User(
                email=data['email'],
                password=data['password']  # Ensure password is hashed in the User model
            )
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify({'status': 'ok', 'message': 'User created', 'id': new_user.id}), 201)
        except KeyError as e:
            return make_response(jsonify({'status': 'error', 'message': f'Missing field: {e}'}), 400)
    def put(self):
        data = request.get_json()
        user_id = data.get('user_id')
        if not user_id:
            return make_response(jsonify({'status': 'error', 'message': 'ID is required'}), 400)
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'status': 'error', 'message': 'User not found'}), 404)

        user.email = data.get('email', user.email)
        # Password should be hashed in the User model
        if 'password' in data:
            user.password = data['password']
        db.session.commit()
        return make_response(jsonify({'status': 'ok', 'message': 'User updated'}), 200)
    def delete(self):
        data = request.get_json()
        user_id = data.get('user_id')
        if not user_id:
            return make_response(jsonify({'status': 'error', 'message': 'ID is required'}), 400)
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'status': 'error', 'message': 'User not found'}), 404)

        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({'status': 'ok', 'message': 'User deleted'}), 200)


#User information name, address, phone number and reservation details
#User can get their own information by user id
#Admin can get any user information by user id
class UserInfoByIdResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'status': 'error', 'message': 'User not found'}), 404)
        
        data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'address': user.address,
            'phone_number': user.phone_number,
            'reservations': []
        }

        for reservation in user.reservations:
            lot = ParkingLot.query.get(reservation.lot_id)
            data['reservations'].append({
                'lot_id': lot.id if lot else None,
                'lot_name': lot.prime_location_name if lot else 'Unknown',
                'spot_id': reservation.spot_id,
                'parking_time': reservation.parking_timestamp.isoformat() if reservation.parking_timestamp else None,
                'leaving_time': reservation.leaving_timestamp.isoformat() if reservation.leaving_timestamp else None,
            })

        return make_response(jsonify({'status': 'ok', 'data': data}), 200)
