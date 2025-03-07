from flask import Blueprint, request, jsonify
from app.config import Config
from app import db, logger
from app.models import Booking, Inventory, Member
from datetime import datetime

bp = Blueprint('booking', __name__)


def validate_request_data(data: dict, required_fields: list) -> tuple[bool, str]:
    """
    Validate incoming request data.

    Args:
        data (dict): Request data.
        required_fields (list): List of required fields.

    Returns:
        tuple: (bool, error message or None)
    """
    for field in required_fields:
        if field not in data:
            return False, f"Missing {field}"
    return True, None


@bp.route('/booking', methods=['GET'])
def get_all_bookings():
    """
    Fetch all booking records.

    Returns:
        JSON response containing booking_id, member_name, and inventory_name.
    """
    try:
        bookings = db.session.query(Booking.id, Member.name, Member.surname, Inventory.title).join(Member).join(
            Inventory).all()
        booking_list = [{'booking_id': b[0], 'member_name': f"{b[1]} {b[2]}", 'inventory_name': b[3]} for b in bookings]
        return jsonify({'bookings': booking_list}), 200
    except Exception as e:
        logger.error(f"Error fetching bookings: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/book', methods=['POST'])
def book_item():
    """
    Book an inventory item for a member.
    """
    try:
        data = request.get_json()
        is_valid, error_message = validate_request_data(data, ['member_id', 'inventory_id'])
        if not is_valid:
            return jsonify({'error': error_message}), 400

        member = Member.query.get(data['member_id'])
        if not member:
            return jsonify({'error': 'Member not found'}), 404

        if member.booking_count >= Config.MAX_BOOKINGS:
            return jsonify({'error': 'Booking limit reached'}), 400

        inventory = Inventory.query.get(data['inventory_id'])
        if not inventory or inventory.remaining_count <= 0:
            return jsonify({'error': 'Item out of stock'}), 400

        booking = Booking(member_id=member.id, inventory_id=inventory.id, booking_date=datetime.utcnow())
        member.booking_count += 1
        inventory.remaining_count -= 1

        db.session.add(booking)
        db.session.commit()

        return jsonify({'message': 'Booking successful', 'booking_id': booking.id}), 200
    except Exception as e:
        logger.error(f"Error booking item: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/cancel', methods=['POST'])
def cancel_booking():
    """
    Cancel a booking.
    """
    try:
        data = request.get_json()
        is_valid, error_message = validate_request_data(data, ['booking_id'])
        if not is_valid:
            return jsonify({'error': error_message}), 400

        booking = Booking.query.get(data['booking_id'])
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        member = Member.query.get(booking.member_id)
        inventory = Inventory.query.get(booking.inventory_id)

        if member:
            member.booking_count = max(0, member.booking_count - 1)

        if inventory:
            inventory.remaining_count += 1

        db.session.delete(booking)
        db.session.commit()

        return jsonify({'message': 'Booking canceled successfully'}), 200
    except Exception as e:
        logger.error(f"Error canceling booking: {e}")
        return jsonify({'error': 'Internal server error'}), 500
