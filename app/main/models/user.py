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
    portfolios = db.relationship('Portfolio', backref='user', lazy=True)

    # @property
    # def password(self):
    #     raise AttributeError('password: write-only field')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"