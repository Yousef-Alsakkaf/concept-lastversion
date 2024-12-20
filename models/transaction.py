from datetime import datetime, timezone
from db_config import db

  #-------------------------
    #   STRIPE SETUP
# Define Database Table Structure
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_method_id = db.Column(db.String(255), nullable=False)
    receipt_email = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(10), default="usd")
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
