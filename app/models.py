from app import db
from datetime import datetime

class Inventory(db.Model):
    """
        Model representing inventory items.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    remaining_count = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)

class Member(db.Model):
    """
        Model representing members.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    booking_count = db.Column(db.Integer, default=0)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

class Booking(db.Model):
    """
        Model representing booking records.
    """
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
