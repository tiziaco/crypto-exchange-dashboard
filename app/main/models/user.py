import re
import uuid
from datetime import datetime

from .. import db
from app.main.models.portfolio import Portfolio

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    portfolios = db.relationship('Portfolio', backref='user', lazy=True)

    def __init__(self, username, email, password):
        self.public_id = str(uuid.uuid4())
        self.username = username
        self.email = self.validate_email(email)
        self.password = password
        self.registered_on = datetime.utcnow()

    def validate_email(self, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email

    # @property
    # def password(self):
    #     raise AttributeError('password: write-only field')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"