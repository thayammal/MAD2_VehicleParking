from flask_restful import Resource
from flask import request, jsonify, make_response
from models import db, ParkingSpot

class ParkingSpotResource(Resource):
    def get(self):
        spots = ParkingSpot.query.all()
        if not spots:
            return make_response(jsonify({'status': 'error', 'message': 'No parking spots found'}), 404)
        
        spot_list = []
        for spot in spots:
            spot_list.append({
                'id': spot.id,
                'spot_number': spot.spot_number,
                'status': spot.status,
                'lot_id': spot.lot_id
            })
        return make_response(jsonify({'status': 'ok', 'spots': spot_list}), 200)

    def post(self):
        data = request.get_json()
        try:
            new_spot = ParkingSpot(
                spot_number=data['spot_number'],
                status=data.get('status', 'A'),
                lot_id=data['lot_id']
            )
            db.session.add(new_spot)
            db.session.commit()
            return make_response(jsonify({'status': 'ok', 'message': 'Parking spot created', 'id': new_spot.id}), 201)
        except KeyError as e:
            return make_response(jsonify({'status': 'error', 'message': f'Missing field: {e}'}), 400)

    def put(self):
        data = request.get_json()
        spot_id = data.get('id')
        if not spot_id:
            return make_response(jsonify({'status': 'error', 'message': 'ID is required'}), 400)
        
        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return make_response(jsonify({'status': 'error', 'message': 'Parking spot not found'}), 404)
        
        spot.spot_number = data.get('spot_number', spot.spot_number)
        spot.status = data.get('status', spot.status)
        spot.lot_id = data.get('lot_id', spot.lot_id)
        db.session.commit()
        return make_response(jsonify({'status': 'ok', 'message': 'Parking spot updated'}), 200)

    def delete(self):
        data = request.get_json()
        spot_id = data.get('id')
        if not spot_id:
            return make_response(jsonify({'status': 'error', 'message': 'ID is required'}), 400)
        
        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return make_response(jsonify({'status': 'error', 'message': 'Parking spot not found'}), 404)
        
        db.session.delete(spot)
        db.session.commit()
        return make_response(jsonify({'status': 'ok', 'message': 'Parking spot deleted'}), 200)


# #updated July15
# Updated July15
class ParkingSpotByLotAndNumber(Resource):
    def get(self, lot_id, spot_num):
        spot = ParkingSpot.query.filter_by(lot_id=lot_id, spot_number=f"Spot-{spot_num}").first()
        if not spot:
            return {'status': 'error', 'message': 'Spot not found'}, 404
        return {
            'status': 'ok',
            'spot': {
                'id': spot.id,
                'lot_id': spot.lot_id,
                'spot_number': spot.spot_number,
                'status': spot.status
            }
        }, 200

# class ParkingSpotsByLot(Resource):
#     def get(self, lot_id):
#         spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
#         if not spots:
#             return {'status': 'error', 'message': 'No spots found for this lot'}, 404
        
#         spot_list = [{
#             'id': s.id,
#             'spot_number': s.spot_number,
#             'status': s.status,
#             'lot_id': s.lot_id
#         } for s in spots]
#         return {'status': 'ok', 'spots': spot_list}, 200
