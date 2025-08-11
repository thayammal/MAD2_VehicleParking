from flask import Flask, request, jsonify
from flask_security import Security, auth_required, roles_accepted, current_user
from flask_restful import Api
from datetime import datetime
import os
from flask_cors import CORS
from sqlalchemy import func
from caching import cache

from models import db, user_datastore, ParkingLot, ParkingSpot, User, Reservation
from routes.parkinglot import ParkingLotResource
from routes.parkingspot import ParkingSpotResource, ParkingSpotByLotAndNumber
from routes.userinfo import UserInfoResource, UserInfoByIdResource


def create_celery(app):
    from celery import Celery
    init_celery = Celery(app.import_name)
    from config import CeleryConfig
    init_celery.config_from_object(CeleryConfig)
    return init_celery



def create_app():
    init_app = Flask(__name__)
    from config import localDev
    init_app.config.from_object(localDev)


    db.init_app(init_app)


    init_api = Api(init_app, prefix='/api')
    CORS(init_app, supports_credentials=True)
    
    # Allow preflight CORS requests
    cache.init_app(init_app)

    from mailing import mail
    mail.init_app(init_app)

    return init_app, init_api

app, api= create_app()
celery_app = create_celery(app)
import tasks

from celery.schedules import crontab
celery_app.conf.beat_schedule = {
    'send-mail-daily-at-6-06pm': {
        'task': 'tasks.send_daily_email_reminders_and_new_lots',
        'schedule': crontab(minute=6, hour=18),
    },

        'monthly-report': {
            'task': 'tasks.send_monthly_report',
            'schedule': crontab(hour=1, minute=0, day_of_month=1),
        },
    }


# Setup restful API
api.add_resource(ParkingLotResource, '/parkinglot')
#api.add_resource(ParkingSpotsByLot, '/parkinglot/<int:lot_id>/spots')
api.add_resource(ParkingSpotByLotAndNumber,'/parkingspot/<int:lot_id>/<int:spot_num>')
api.add_resource(ParkingSpotResource, '/parkingspot')
api.add_resource(UserInfoResource, '/userinfo')
api.add_resource(UserInfoByIdResource, '/search/userinfo/<int:user_id>')

Security(app, user_datastore)


from flask import jsonify
import tasks

# @app.route('/test_celery', methods=['GET'])
# def test_celery():
#     from models import User
#     users = User.query.all()
#     if not users:
#         return {'status': 'error', 'message': 'No users found'}, 404
#     last = {}
#     for user in users:
#         result = tasks.send_a_mail.delay(user.email)
#         last = {'user': user.email, 'task_id': result.id}
#     return {'status': 'ok', 'last_task': last}, 202

# @app.route('/test_celery', methods=['GET'])
# def test_celery():
#     # result = tasks.query_lotdb.delay()
#     # while not result.ready():
#     #     pass
#     # return {'status': 'ok', 'message':'Celery task started', 'task_id':result.id, 'task_result':result.result},200
#     from models import User
#     users = User.query.all()
#     if not users:
#         return {'status':'error', 'message':'No users found'}, 404
#     for user in users:
#         print(f"User:{user.username}, Email : {user.email}")
#         result = tasks.send_a_mail.delay(user.email)
#         print(f"Task ID: {result.id}")
#         while not result.ready():
#             pass
#     return {'status': 'ok', 'meassagre': 'Celery task started', 'task_id':result.id, 'task_result':result.result}, 200


@app.route('/trigger_daily_reminders', methods=['GET'])
def trigger_daily_reminders():
    """
    Enqueue the daily reminder task immediately (for manual testing).
    Responds with a task ID.
    """
    result = tasks.send_daily_email_reminders_and_new_lots.delay()
    return jsonify({"status": "queued", "task_id": result.id}), 202


@app.route('/trigger_monthly_report', methods=['GET'])
def trigger_monthly_report():
    task = tasks.send_monthly_report.delay()
    return jsonify({"status": "queued", "task_id": task.id}), 202

# @app.route('/task_status/<task_id>', methods=['GET'])
# def task_status(task_id):
#     """
#     Lookup task state and result using the task ID.
#     """
#     result = AsyncResult(task_id, app=celery)
#     response = {"task_id": task_id, "status": result.state}
#     if result.ready():
#         response["result"] = result.result
#     return jsonify(response), 200



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return {'status': 'error', 'message': 'Message is required'}, 400
        return {'status': 'ok', 'message': f"Received message: {data}"}, 200
    return {'status': 'ok', 'message': 'Welcome to the Parking Management System API'}, 200



@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return {'status': 'error', 'message': 'Username is required'}, 400
    email = data.get('email')
    if not email:
        return {'status': 'error', 'message': 'Email is required'}, 400
    password = data.get('password')
    if not password:
        return {'status': 'error', 'message': 'Password is required'}, 400
    address = data.get('address')
    phone_number = data.get('phone_number') 

    if not user_datastore.find_user(email=email):
        new_user = user_datastore.create_user(email=email, username=username, password=password, address=address, phone_number=phone_number)
        user_datastore.add_role_to_user(new_user, 'user')
        db.session.commit()
        return {'status': 'ok', 'message': 'User created successfully'}
    return {'status': 'error', 'message': 'User already exists'}, 400


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Extract email and password
    email = data.get('email')
    password = data.get('password')

    # Validate inputs
    if not email:
        return {'status': 'error', 'message': 'Email is required'}, 400
    if not password:
        return {'status': 'error', 'message': 'Password is required'}, 400

    # Find user by email
    user = user_datastore.find_user(email=email)
    if not user:
        return {'status': 'error', 'message': 'User not found'}, 404

    # Password check (assuming plain-text for now; see note below)
    if user.password != password:
        return {'status': 'error', 'message': 'Invalid password'}, 401

    # Generate auth token (assuming method exists)
    auth_token = user.get_auth_token()

    # Update user login details
    user.last_login_at = user.current_login_at
    user.current_login_at = datetime.utcnow()
    user.last_login_ip = user.current_login_ip      
    user.current_login_ip = request.remote_addr
    user.login_count = (user.login_count or 0) + 1  
    db.session.commit()

    # Return success response
    return {
        'status': 'ok',
        'message': 'Login successful',
        'auth_token': auth_token,
        'role': user.roles[0].name if user.roles else None,
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
    }, 200

@app.route('/test', methods=['GET'])
@auth_required('token')
# @roles_required('user', 'admin') # AND
@roles_accepted('user', 'admin') # OR
def test():
    # found_user = User.query.filter_by(id=1).first()
    # print(found_user.email)
    return {'status': 'ok', 'message': 'Test successful', 'email': current_user.username}, 200



@app.route('/userinfo', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth_required('token')
@roles_accepted('admin')
def get_users():
    if request.method == 'GET':
    # Ensure method is GET  
        users = User.query.filter(Users.role.any(name ='user')).all()
        if users:
            user_list = []
            for user in users:
                user_list.append({
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'address': user.address,
                    'phone_number': user.phone_number,
                    'last_login_at': user.last_login_at,
                    'roles': [role.name for role in user.roles]
                })
            return {'status': 'ok', 'message': 'Users retrieved successfully', 'users': user_list}, 200
        return {'status': 'error', 'message': 'No users found'}, 404
    
    elif request.method == 'POST':
        data = request.get_json() or {}
        missing = [f for f in ('email', 'password') if f not in data]
        if missing:
            return {'status': 'error', 'message': f"Missing field(s): {', '.join(missing)}"}, 400
        new = User(email=data['email'], password=data['password'])
        db.session.add(new)
        db.session.commit()
        return {'status': 'ok', 'message': 'User created', 'id': new.id}, 201
    
    elif request.method == 'PUT':
        data = request.get_json()
        user_id = data.get('user_id')
        if not user_id:
            return {'status': 'error', 'message': 'Parking lot ID is required'}, 400

        user = User.query.get(user_id)
        if not user:
            return {'status': 'error', 'message': 'Parking lot not found'}, 404

        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.address = data.get('address', user.address)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.password = data.get('password', user.password)
        db.session.commit()
        return {'status': 'ok', 'message': 'User profile updated', 'username': user.username}, 200

           
    elif request.method == 'DELETE':
        data = request.get_json() or {}
        if not data.get('id'):
            return {'status': 'error', 'message': 'ID is required'}, 400
        user = User.query.get(data['id'])
        if not user:
            return {'status': 'error', 'message': 'User not found'}, 404
        
        db.session.delete(user)
        db.session.commit()
        return {'status': 'ok', 'message': 'User deleted'}, 200
    
    # Should never reach here
    return {'status': 'error', 'message': 'Unsupported method'}, 405




@app.route('/parkinglot', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth_required('token')
@roles_accepted('admin')
def parking_lot():
    if request.method == 'GET':
        lots = ParkingLot.query.all()
        result = []
        for lot in lots:
            result.append({
                "id": lot.id,
                "prime_location_name": lot.prime_location_name,
                "price": lot.price,
                "address": lot.address,
                "pin_code": lot.pin_code,
                "number_of_spots": lot.number_of_spots,
                "available_spots": lot.available_spots,
                "spots": [
                    {
                        "id": s.id,
                        "spot_number": s.spot_number,
                        "status": s.status
                    } for s in lot.spots
                ]
            })
        return {"lots": result}, 200 

    elif request.method == 'POST':
        data = request.get_json()
        required_fields = ['prime_location_name', 'price', 'address', 'pin_code', 'number_of_spots']
        for field in required_fields:
            if not data.get(field):
                return {'status': 'error', 'message': f'{field} is required'}, 400

        new_lot = ParkingLot(
            prime_location_name=data['prime_location_name'],
            price=data['price'],
            address=data['address'],
            pin_code=data['pin_code'],
            number_of_spots=data['number_of_spots'],

        )
        db.session.add(new_lot)
        db.session.flush()
        print("Lot ID after flush:", new_lot.id)
        # Create associated parking spots
        for i in range(1, new_lot.number_of_spots + 1):
            spot = ParkingSpot(
            lot_id=new_lot.id,
            status='A',
            spot_number= f"Spot-{i}"  # Example: S001, S002, ...
        )
            db.session.add(spot)
        db.session.commit()
        return {'status': 'ok', 'message': 'Parking lot created', 'id': new_lot.id}, 201

    elif request.method == 'PUT':
        data = request.get_json()
        lot_id = data.get('id')
        if not lot_id:
            return {'status': 'error', 'message': 'Parking lot ID is required'}, 400

        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {'status': 'error', 'message': 'Parking lot not found'}, 404

        lot.prime_location_name = data.get('prime_location_name', lot.prime_location_name)
        lot.price = data.get('price', lot.price)
        lot.address = data.get('address', lot.address)
        lot.pin_code = data.get('pin_code', lot.pin_code)
        lot.number_of_spots = data.get('number_of_spots', lot.number_of_spots)
        db.session.commit()
        return {'status': 'ok', 'message': 'Parking lot updated', 'id': lot.id}, 200

    elif request.method == 'DELETE':
        data = request.get_json()
        lot_id = data.get('id')
        if not lot_id:
            return {'status': 'error', 'message': 'Parking lot ID is required'}, 400

        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {'status': 'error', 'message': 'Parking lot not found'}, 404

        db.session.delete(lot)
        db.session.commit()
        return {'status': 'ok', 'message': 'Parking lot deleted', 'id': lot.id}, 200



@app.route('/api/available-spot', methods=['GET'])
@cache.cached(timeout=60)
@auth_required('token')
def get_available_spot():
    lot_id = request.args.get('lot_id')
    if not lot_id:
        return jsonify({'status': 'error', 'message': 'Lot ID is required'}), 400

    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not spot:
        return jsonify({'status': 'error', 'message': 'No available spots'}), 404

    return jsonify({'status': 'ok', 'spot_id':spot.id, 'spot_number': spot.spot_number})



@app.route('/api/book-spot', methods=['POST'])
@auth_required('token')
@roles_accepted('user', 'admin')
def book_spot():
    try:
        data = request.get_json() or {}

        lot_id = data.get('lot_id')
        spot_number = data.get('spot_id')
        user_id = data.get('user_id')
        vehicle_number = data.get('vehicle_number')

        # Validate presence
        if not all([lot_id, spot_number, user_id, vehicle_number]):
            return {'status': 'error', 'message': 'Missing required fields'}, 400

        # Get and validate lot
        lot = db.session.get(ParkingLot, lot_id)
        if not lot:
            return {'status': 'error', 'message': 'Invalid lot ID'}, 404

        # Get and validate spot
        spot = ParkingSpot.query.filter_by(lot_id=lot_id, spot_number=spot_number).first()
        if not spot or spot.status != 'A':
            return {'status': 'error', 'message': 'Selected spot is not available'}, 400

        # Mark as occupied
        spot.status = 'O'
        available_spots = lot.available_spots
        #lot.number_of_spots = max(lot.number_of_spots - 1, 0)

        #  Create reservation
        reservation = Reservation(
            lot_id=lot_id,
            spot_id=spot.id,
            user_id=user_id,
            vehicle_number=vehicle_number,
            parking_timestamp=datetime.utcnow()
        )

        db.session.add(reservation)
        db.session.commit()

        return {'status': 'success', 'message': f'Spot {spot.spot_number} reserved successfully'}

    except Exception as e:
        print(" Error during booking:", str(e))
        db.session.rollback()
        return {'status': 'error', 'message': str(e)}, 500



@app.route('/api/recent-reservations', methods=['GET'])
@auth_required('token')
@roles_accepted('user', 'admin')
def get_recent_reservations():
    print('user email is: ', current_user.email)
    user_id = current_user.id
    reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.parking_timestamp.desc()).limit(3).all()
    result = []
    for res in reservations:
        print(' RES:', res.user_id, res.parking_timestamp)
        result.append({
            'lot_id': res.lot_id,
            'spot_id': res.spot_id,
            'location': res.lot.prime_location_name,
            'vehicle_number': res.vehicle_number,
            'parking_timestamp': res.parking_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'reservation_status': res.reservation_status
        })

    return jsonify({'recent': result}), 200




@app.route('/api/release-spot', methods=['POST'])
def release_spot():
    data = request.get_json()
    if data is None:
        return jsonify({'message': 'Invalid JSON'}), 400

    lot_id = data.get('lot_id')
    spot_id = data.get('spot_id')
    user_id = data.get('user_id')

    if not all([lot_id, spot_id, user_id]):
        return jsonify({'message': 'Missing lot_id, spot_id, or user_id'}), 400

    # Find active reservation
    reservation = Reservation.query.filter_by(
        lot_id=lot_id,
        spot_id=spot_id,
        user_id=user_id,
        leaving_timestamp=None
    ).first()

    if not reservation:
        return jsonify({'message': 'Active reservation not found'}), 404

    # Mark release timestamp
    release_time = datetime.now()
    reservation.leaving_timestamp = release_time

    # Calculate duration and cost
    parking_time = reservation.parking_timestamp
    duration_hours = (release_time - parking_time).total_seconds() / 3600

    # Optionally, fetch price from Spot model if not already in reservation
    spot = ParkingLot.query.filter_by(id=lot_id).first()
    price_per_hour = spot.price if spot else 10  # fallback price

    total_cost = round(duration_hours * price_per_hour, 2)
    reservation.total_cost = total_cost
    reservation.parking_cost = total_cost
    reservation.reservation_status = 'Parked Out'
    db.session.commit()

    return jsonify({
        'message': 'Spot released successfully',
        'lot_id': lot_id,
        'spot_id': spot_id,
        'user_id': user_id,
        'parking_timestamp': parking_time,
        'release_timestamp': release_time,
        'total_cost': total_cost
    }), 200

@app.route('/api/user-summary')
def user_summary():
    user_id = current_user.id
    print("🔍 User ID received:", user_id)

    # Cost summary by location
    cost_data = (
        db.session.query(ParkingLot.prime_location_name, db.func.sum(Reservation.parking_cost))
        .join(Reservation, ParkingLot.id == Reservation.lot_id)
        .filter(Reservation.user_id == user_id)
        .group_by(ParkingLot.prime_location_name)
        .all()
    )

    cost_summary = [{"location": loc, "total_cost": float(cost or 0)} for loc, cost in cost_data]

    # Reservation count summary
    count_data = (
        db.session.query(ParkingLot.prime_location_name, db.func.count(Reservation.id))
        .join(Reservation, ParkingLot.id == Reservation.lot_id)
        .filter(Reservation.user_id == user_id)
        .group_by(ParkingLot.prime_location_name)
        .all()
    )

    reservation_summary = [{"location": loc, "count": count} for loc, count in count_data]
    print('cost_summary', cost_data)
    return jsonify({
        "cost_by_location": cost_summary,
        "reservation_by_location": reservation_summary
    })



@app.route('/parkingspot', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth_required('token')
@roles_accepted('admin')
def spot_lot():
    if request.method == 'GET':
        spots = ParkingSpot.query.all()
        if spots:
            spot_list = []
            for spot in spots:
                spot_list.append({
                    'id': spot.id,
                    'lot_id': spot.lot_id,
                    'spot_number': spot.spot_number,
                    'status': spot.status
                    #'created_at': spot.created_at
                })
            return {'status': 'ok', 'message': 'Spot lots retrieved successfully', 'spots': spot_list}, 200
        return {'status': 'error', 'message': 'No spot lots found'}, 404

    elif request.method == 'POST':
        data = request.get_json()
        required_fields = ['lot_id', 'spot_number']
        for field in required_fields:
            if not data.get(field):
                return {'status': 'error', 'message': f'{field} is required'}, 400

        new_spot = ParkingSpot(
            lot_id=data['lot_id'],
            spot_number=data['spot_number'],
            status=data.get('status', "A")
        )
        db.session.add(new_spot)
        db.session.commit()
        return {'status': 'ok', 'message': 'Spot lot created', 'id': new_spot.id}, 201

    elif request.method == 'PUT':
        data = request.get_json()
        spot_id = data.get('id')
        if not spot_id:
            return {'status': 'error', 'message': 'Spot lot ID is required'}, 400

        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return {'status': 'error', 'message': 'Spot lot not found'}, 404

        spot.parking_lot_id = data.get('parking_lot_id', spot.parking_lot_id)
        spot.spot_number = data.get('spot_number', spot.spot_number)
        spot.is_available = data.get('is_available', spot.is_available)
        db.session.commit()
        return {'status': 'ok', 'message': 'Spot lot updated', 'id': spot.id}, 200

    elif request.method == 'DELETE':
        data = request.get_json()
        spot_id = data.get('id')
        if not spot_id:
            return {'status': 'error', 'message': 'Spot lot ID is required'}, 400

        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return {'status': 'error', 'message': 'Spot lot not found'}, 404

        db.session.delete(spot)
        db.session.commit()
        return {'status': 'ok', 'message': 'Spot lot deleted', 'id': spot.id}, 200

@app.route('/parkingspot/<int:lot_id>/<int:spot_num>', methods=['GET'])
@auth_required('token')
@roles_accepted('admin')
def get_spot_by_lot_and_number(lot_id, spot_num):
    print(lot_id)
    print(spot_num)
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, spot_number=f"Spot-{spot_num}").first()
    
    if not spot:
        return {'status': 'error', 'message': 'Parking spot not found'}, 404

    spot_data = {
        'id': spot.id,
        'lot_id': spot.lot_id,
        'spot_number': spot.spot_number,
        'status': spot.status
    }
    return {'status': 'ok', 'spot': spot_data}, 200



@app.route('/api/search/userinfo/<int:user_id>', methods=['GET'])
@auth_required('token')
@roles_accepted('admin', 'user')
def get_user_info(user_id):
    print('user email is: ', current_user.email)
    user_id = current_user.id
    reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.parking_timestamp.desc()).all()
    result = []
    for res in reservations:
        print('RES:', res.user_id, res.parking_timestamp)
        result.append({
            'lot_id': res.lot_id,
            'spot_id': res.spot_id,
            'location': res.lot.prime_location_name,
            'vehicle_number': res.vehicle_number,
            'parking_timestamp': res.parking_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'leaving_timestamp': res.leaving_timestamp
        })

    return jsonify({'recent': result}), 200

@app.route('/api/parkingspot/<int:lot_id>/<int:spot_num>/details')
@cache.cached(timeout=60)
@auth_required('token')
@roles_accepted('admin')
def get_spot_details(lot_id, spot_num):
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, spot_number=(f'Spot-{spot_num}')).first()
    lot = ParkingLot.query.get(lot_id)

    if not spot:
        return jsonify({'status': 'error', 'message': 'Spot not found'}), 404

    if spot.status != 'O':
        return jsonify({'status':'ok', 'spot':{'id':spot.id,'status':spot.status}}), 200

    reservation = Reservation.query.filter_by(spot_id=spot.id)\
        .order_by(Reservation.parking_timestamp.desc()).first()
    if not reservation:
        return jsonify({'status':'ok','spot':{'id':spot.id,'status':spot.status}}), 200
    
    leaving_timestamp = reservation.leaving_timestamp or datetime.now()
    duration_hours = (leaving_timestamp - reservation.parking_timestamp).total_seconds()/3600
    rate = lot.price#spot.lot.price if hasattr(spot.lot, 'hourly_rate') else 0
    cost = round(duration_hours * rate, 2)
    print(rate)
    return jsonify({
        'status': 'ok',
        'spot': {
            'id': spot.id,
            'status': spot.status,
            'parking_timestamp': reservation.parking_timestamp.isoformat(),
            'leaving_timestamp': reservation.leaving_timestamp.isoformat() if reservation.leaving_timestamp else None,
            'username': reservation.user.username,
            'vehicle_number': reservation.vehicle_number,
            'estimated_cost': cost
        }
    }), 200



@app.route('/admin/spot-summary')
@auth_required('token')
@roles_accepted('admin')
def spot_summary():
    lots = ParkingLot.query.all()
    summary = []
    for lot in lots:
        available = sum(1 for s in lot.spots if s.status == 'A')
        occupied = sum(1 for s in lot.spots if s.status == 'O')
        summary.append({
            "location": lot.prime_location_name,
            "available": available,
            "occupied": occupied
        })
    return jsonify(summary), 200

@app.route('/admin/cost-summary')
@auth_required('token')
@roles_accepted('admin')
def cost_summary():
    print(request.headers.get("Authorization"))

     # Join Reservation with ParkingLot and filter by status
    results = (
        db.session.query(
            ParkingLot.prime_location_name.label('location'),
            func.sum(Reservation.parking_cost).label('total_cost')
        )
        .join(ParkingLot, Reservation.lot_id == ParkingLot.id)
        .filter(Reservation.reservation_status == 'Parked Out')
        .group_by(ParkingLot.prime_location_name)
        .all()
    )

    # Convert to JSON-serializable format
    output = [{"location": row.location, "total_cost": float(row.total_cost or 0)} for row in results]

    return jsonify(output), 200

if __name__ == '__main__':

    app.run()