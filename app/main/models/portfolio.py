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
    entry_date = db.Column(db.DateTime, nullable=False)
    exit_date = db.Column(db.DateTime, nullable=True)
    symbol = db.Column(db.String(10), nullable=False)
    side = db.Column(db.String(10), nullable=False)
    buy_quantity = db.Column(db.Integer, nullable=False)
    sell_quantity = db.Column(db.Integer, nullable=False)
    avg_bought = db.Column(db.Integer, nullable=False)
    avg_sold = db.Column(db.Integer, nullable=False)
    buy_commission = db.Column(db.Integer, nullable=False)
    buy_quantity = db.Column(db.Integer, nullable=False)
    is_open = db.Column(db.Boolean, default = True, nullable=False)
    sell_commission = db.relationship('Transaction', backref='portfolio', lazy=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)

    current_price = 0;

    def __repr__(self):
        return f"Position('{self.symbol}', {self.quantity})"
    
    @property
    def market_value(self):
        """
        Return the market value (respecting the direction) of the
        Position based on the current price available to the Position.
        """
        return self.current_price * abs(self.net_quantity)

    @property
    def avg_price(self):
        """
        The average price paid for all assets on the long or short side.
        """
        if self.net_quantity == 0:
            return 0.0
        elif self.action =='BOT':
            return (self.avg_bought * self.buy_quantity + self.buy_commission) / self.buy_quantity
        else: # action == "SLD"
            return (self.avg_sold * self.sell_quantity - self.sell_commission) / self.sell_quantity

    @property
    def net_quantity(self):
        """
        The difference in the quantity of assets bought and sold to date.
        """
        return abs(self.buy_quantity - self.sell_quantity)

    @property
    def total_bought(self):
        """
        Calculates the total average cost of assets bought.
        """
        return self.avg_bought * self.buy_quantity

    @property
    def total_sold(self):
        """
        Calculates the total average cost of assets sold.
        """
        return self.avg_sold * self.sell_quantity

    @property
    def net_total(self):
        """
        Calculates the net total average cost of assets
        bought and sold.
        """
        return self.total_sold - self.total_bought

    @property
    def commission(self):
        """
        Calculates the total commission from assets bought and sold.
        """
        return self.buy_commission + self.sell_commission

    @property
    def net_incl_commission(self):
        """
        Calculates the net total average cost of assets bought
        and sold including the commission.
        """
        return self.net_total - self.commission

    @property
    def realised_pnl(self):
        """
        Calculates the profit & loss (P&L) that has been 'realised' via
        two opposing asset transactions in the Position to date.
        """
        if self.action == 'BOT':
            if self.sell_quantity == 0:
                return 0.0
            else:
                return (
                    ((self.avg_sold - self.avg_bought) * self.sell_quantity) -
                    ((self.sell_quantity / self.buy_quantity) * self.buy_commission) -
                    self.sell_commission
                )
        elif self.action == 'SLD':
            if self.buy_quantity == 0:
                return 0.0
            else:
                return (
                    ((self.avg_sold - self.avg_bought) * self.buy_quantity) -
                    ((self.buy_quantity / self.sell_quantity) * self.sell_commission) -
                    self.buy_commission
                )
        else:
            return self.net_incl_commission

    @property
    def unrealised_pnl(self):
        """
        Calculates the profit & loss (P&L) that has yet to be 'realised'
        in the remaining non-zero quantity of assets, due to the current
        market price.
        """
        return (self.current_price - self.avg_price) * self.net_quantity

    @property
    def total_pnl(self):
        """
        Calculates the sum of the unrealised and realised profit & loss (P&L).
        """
        return self.realised_pnl + self.unrealised_pnl