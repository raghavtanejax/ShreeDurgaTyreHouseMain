from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

class Tyre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(150), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def stock_status(self):
        if self.stock <= 0:
            return "Out of Stock"
        elif self.stock <= 10:
            return "Low Stock"
        else:
            return "In Stock"

class QuoteRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    vehicle_type = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primary_contact = db.Column(db.String(50), default="+91 9876543210")
    secondary_contact = db.Column(db.String(50), default="+91 1234567890")
    physical_address = db.Column(db.Text, default="NH-44, Industrial Area, Delhi")
    google_maps_url = db.Column(db.String(255), default="https://maps.google.com/")
    hindi_english_toggle = db.Column(db.Boolean, default=True)

class DispatchActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    tyre_details = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, default=0.0)
    amount_received = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default="Pending") # Pending, Dispatched, Delivered
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def amount_left(self):
        return max(0.0, self.total_amount - self.amount_received)

