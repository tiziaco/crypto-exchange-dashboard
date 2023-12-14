from .. import db
from datetime import datetime

class Portfolio(db.Model):
    __tablename__ = "portfolio"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exchange = db.Column(db.String(50), nullable=False)
    transactions = db.relationship('Transaction', backref='portfolio', lazy=True)
    positions = db.relationship('Position', backref='portfolio', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'exchange': self.exchange,
            'transactions': len(self.transactions)
        }

    def __repr__(self):
        return f"Portfolio('{self.name}')"


class Transaction(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False)
    pair = db.Column(db.String(10), nullable=False)
    side = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)

    def __init__(self, date=None, *args, **kwargs):
        if date is None:
            date = datetime.utcnow()
        super().__init__(date=date, *args, **kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'pair': self.pair,
            'side': self.side,
            'price': self.price,
            'quantity': self.quantity,
            'amount': self.amount
        }

    def __repr__(self):
        return f"Transaction('{self.pair}', {self.quantity}, '{self.side}', {self.date})"


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    transactions = db.relationship('Transaction', backref='portfolio', lazy=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)

    def __repr__(self):
        return f"Position('{self.symbol}', {self.quantity})"