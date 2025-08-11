from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import current_user
from models import db, ParkingLot, ParkingSpot
from datetime import datetime
from sqlalchemy import or_


class ParkingLotResource(Resource):
    def get(self):
        q = request.args.get('query', '').strip()
        pc = request.args.get('pincode', '').strip()


        query = ParkingLot.query
        if q:
            query = query.filter(
                or_(
                    ParkingLot.address.ilike(f'%{q}%'),
                    ParkingLot.prime_location_name.ilike(f'%{q}%')
                )
            )
        elif pc:
            query = query.filter(ParkingLot.pin_code == pc)
        
        else:
            query = query

        lots = query.all()

        #lots = ParkingLot.query.all()
        if not lots:
            return make_response(jsonify({'status': 'error', 'message': 'No parking lots found'}), 404)
        
        lot_list = []
        for lot in lots:
            lot_list.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'price': lot.price,
                'address': lot.address,
                'pin_code': lot.pin_code,
                'number_of_spots': lot.number_of_spots,
                'available_spots': lot.available_spots,
                'created_at': lot.created_at,
                 "spots": [
                    {
                        "id": s.id,
                        "spot_number": s.spot_number,
                        "status": s.status
                    } for s in lot.spots
                 ]

            })
        #print(lot_list)
        return make_response(jsonify({'status': 'ok', 'lots': lot_list}), 200)

    def post(self):
        data = request.get_json()
        try:
            new_lot = ParkingLot(
                prime_location_name=data['prime_location_name'],
                price=data['price'],
                address=data['address'],
                pin_code=data['pin_code'],
                number_of_spots=data['number_of_spots']
            )
            db.session.add(new_lot)
            db.session.commit()
            print('lot id is:', new_lot.id)
            for i in range(1, new_lot.number_of_spots + 1):
                spot = ParkingSpot(
                    lot_id=new_lot.id,
                    status='A',
                    spot_number= f"Spot-{i}"
                )
                db.session.add(spot)

            db.session.commit()
            return make_response(jsonify({'status': 'ok', 'message': 'Parking lot created', 'id': new_lot.id}), 201)


        except KeyError as e:
            db.session.rollback()
            return make_response(jsonify({'status': 'error', 'message': f'Missing field: {e}'}), 400)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'status': 'error', 'message': str(e)}), 500)
        
    def put(self):
        data = request.get_json()
        lot_id = data.get('id')
        if not lot_id:
            return make_response(jsonify({'status': 'error', 'message': 'ID is required'}), 400)
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return make_response(jsonify({'status': 'error', 'message': 'Parking lot not found'}), 404)

        lot.prime_location_name = data.get('prime_location_name', lot.prime_location_name)
        lot.price = data.get('price', lot.price)
        lot.address = data.get('address', lot.address)
        lot.pin_code = data.get('pin_code', lot.pin_code)
        lot.number_of_spots = data.get('number_of_spots', lot.number_of_spots)
        db.session.commit()
        return make_response(jsonify({'status': 'ok', 'message': 'Parking lot updated'}), 200)

    def delete(self):
        data = request.get_json()
        lot_id = data.get('id')
        if not lot_id:
            return make_response(jsonify({'status': 'error', 'message': 'ID is required'}), 400)
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return make_response(jsonify({'status': 'error', 'message': 'Parking lot not found'}), 404)
        db.session.delete(lot)
        db.session.commit()
        return make_response(jsonify({'status': 'ok', 'message': 'Parking lot deleted'}), 200)
