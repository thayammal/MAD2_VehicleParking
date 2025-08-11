from flask_restful import Resource
from flask import request, jsonify
from models import db, Reservation, ParkingSpot
from datetime import datetime

class ReleaseSpotResource(Resource):
    def post(self):
        data = request.get_json()
        lot_id = data.get('lot_id')
        spot_id = data.get('spot_id')
        user_id = data.get('user_id')

        if not lot_id or not spot_id:
            return {'status': 'error', 'message': 'lot_id and spot_id are required'}, 400

        # Find the active reservation
        reservation = Reservation.query.filter_by(
            lot_id=lot_id, spot_id=spot_id, release_timestamp=None
        ).first()

        if not reservation:
            return {'status': 'error', 'message': 'Active reservation not found'}, 404

        # Calculate release timestamp and cost
        now = datetime.utcnow()
        duration_hours = (now - reservation.parking_timestamp).total_seconds() / 3600
        total_cost = round(duration_hours * reservation.price_per_hour, 2)

        # Update reservation
        reservation.release_timestamp = now
        reservation.total_cost = total_cost
        db.session.commit()

        # Free the parking spot
        spot = ParkingSpot.query.get(spot_id)
        if spot:
            spot.status = 'A'  # Available
            db.session.commit()

        return {
            'status': 'ok',
            'message': 'Spot released',
            'data': {
                'lot_id': lot_id,
                'spot_id': spot_id,
                'parking_timestamp': reservation.parking_timestamp,
                'release_timestamp': now,
                'total_cost': total_cost
            }
        }, 200
