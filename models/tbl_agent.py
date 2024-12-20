from datetime import datetime, timezone
from db_config import db

class TblAgent(db.Model):
    __tablename__ = 'tbl_agent'

    agent_id = db.Column(db.BigInteger, primary_key=True)  # Primary key column
    agent_name = db.Column(db.String(255), nullable=False)  # Not null
    gender = db.Column(db.String(10))  # Can be nullable, with a constraint to validate values
    image_url = db.Column(db.String(255), nullable=False)  # Not null
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)  # Default timestamp
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))  # Updated timestamp
    agent_prompt = db.Column(db.Text, nullable=False)  # Not null
    agent_role = db.Column(db.String(255), nullable=False)  # Not null

    