from datetime import datetime, timezone
from db_config import db

class ChatSession(db.Model):
    __tablename__ = 'tbl_chat_session'

    session_id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    custom_prompt = db.Column(db.Text)
    history = db.Column(db.JSON, default=[])
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))