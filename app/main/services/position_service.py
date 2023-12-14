from flask import jsonify
from app.main import db
from app.main.models.portfolio import Position, Transaction
from datetime import datetime


def process_transaction(trade_pair, quantity, price, side):
    # Retrieve existing position for the trading pair
    existing_position = Position.query.filter_by(symbol=trade_pair, is_open=True).first()

    if side == 'buy':
        if existing_position:
            # Update existing position for buy transaction
            update_position(existing_position, quantity, price)
        else:
            # Create a new long position for the trading pair
            create_position(trade_pair, quantity, price, side='long')
    elif side == 'sell':
        if existing_position:
            # Update existing position for sell transaction
            update_position(existing_position, -quantity, price)
            # Check if position should be closed
            if existing_position.net_quantity == 0:
                close_position(existing_position)
        else:
            # Create a new short position for the trading pair
            create_position(trade_pair, -quantity, price, side='short')

def create_position(trade_pair, quantity, price, side):
    new_position = Position(
        entry_date=datetime.utcnow(),
        symbol=trade_pair,
        buy_quantity=max(quantity, 0) if side == 'long' else 0,
        sell_quantity=-min(quantity, 0) if side == 'short' else 0,
        avg_bought=price if side == 'long' else 0,
        avg_sold=price if side == 'short' else 0,
        buy_commission=0,
        sell_commission=0,
        is_open=True,
        current_price=0
    )
    db.session.add(new_position)
    db.session.commit()

def update_position(position, quantity, price):
    # Update position details based on the transaction
    if quantity > 0:  # Buy transaction
        position.buy_quantity += quantity
        position.avg_bought = (position.avg_bought * position.buy_quantity + price) / position.buy_quantity
    elif quantity < 0:  # Sell transaction
        position.sell_quantity -= quantity
        position.avg_sold = (position.avg_sold * position.sell_quantity - price) / position.sell_quantity

    position.current_price = price  # Update current price
    db.session.commit()

def close_position(position):
    # Close the position by updating is_open to False
    position.is_open = False
    position.exit_date = datetime.utcnow()
    db.session.commit()