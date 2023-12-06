from app import db
from datetime import datetime

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transactions = db.relationship('Transaction', backref='portfolio', lazy=True)
    positions = db.relationship('Position', backref='portfolio', lazy=True)

    def __repr__(self):
        return f"Portfolio('{self.name}')"

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)

    def __repr__(self):
        return f"Position('{self.symbol}', {self.quantity})"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    pair = db.Column(db.String(10), nullable=False)
    side = db.Column(db.String(10), nullable=False)  # 'buy' or 'sell'
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)

    def __repr__(self):
        return f"Transaction('{self.pair}', {self.quantity}, '{self.side}', {self.date})"