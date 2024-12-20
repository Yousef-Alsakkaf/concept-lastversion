from datetime import datetime, timezone
from db_config import db

class tbl_prompt(db.Model):
    __tablename__ = 'tbl_prompt'

    prompt_id = db.Column(db.BigInteger, primary_key=True)
    role = db.Column(db.String(255), nullable=True)
    prompt = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    user_id = db.Column(db.BigInteger, nullable=True)
    company_id = db.Column(db.BigInteger, nullable=True)