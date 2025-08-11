from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
from datetime import datetime

db = SQLAlchemy()


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reservations = db.relationship('Reservation', backref='user', lazy=True)

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)

    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    
    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic'))
    
user_datastore = SQLAlchemyUserDatastore(db, User, Role)


class ParkingLot(db.Model):
    __tablename__ = 'parkinglots'
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    number_of_spots = db.Column(db.Integer, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    #created_at = db.Column(db.DateTime())

    spots = db.relationship('ParkingSpot', backref='lot', cascade="all, delete", lazy=True)
    @property
    def available_spots(self):
        # Return the count of spots that are available
        return sum(1 for spot in self.spots if spot.status == 'A')
    def __repr__(self):
        return f"<ParkingLot {self.prime_location_name}>"


class ParkingSpot(db.Model):
    __tablename__ = 'parkingspots'
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parkinglots.id'), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')  # A = Available, O = Occupied
    spot_number = db.Column(db.String(20), nullable=True)
    reservations = db.relationship('Reservation', backref='spot', lazy=True)

    def __repr__(self):
        return f"<Spot {self.id} - Lot {self.lot_id} - {self.status}>"


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parkinglots.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parkingspots.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, nullable=True)
    reservation_status = db.Column(db.String(30), nullable=False, default = 'Release' )
    vehicle_number = db.Column(db.String(20), nullable=False)  
    lot = db.relationship('ParkingLot', backref='reservations', lazy=True)

    def __repr__(self):
        return f"<Reservation {self.id} - Spot {self.spot_id} - User {self.user_id}>"
