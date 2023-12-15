from datetime import datetime
from app.main.models.user import User
from app.main.models.portfolio import Portfolio, Transaction, Position
from app.main import db

def create_test_user():
    user = User(
        username='test_user',
        email='test@example.com',
        password='12345',
    )
    save_changes(user)
    return user

def create_test_portfolio(user_id):
    portfolio = Portfolio(
        name='test_portfolio',
        user_id=user_id,
        exchange = 'Binance Test'
    )
    save_changes(portfolio)
    return portfolio

def create_test_position(transaction, side):
    position = Position(
        entry_date=datetime.utcnow(),
        portfolio_id = transaction.portfolio_id,
        symbol=transaction.pair,
        side = side,
        buy_quantity=max(transaction.quantity, 0) if side == 'long' else 0,
        sell_quantity=-min(transaction.quantity, 0) if side == 'short' else 0,
        avg_bought=transaction.price if side == 'long' else 0,
        avg_sold=transaction.price if side == 'short' else 0,
        buy_commission=0,
        sell_commission=0,
        is_open=True,
        current_price=0
    )
    return position

def create_test_portfolio_with_transaction():
    # Create a test user
    user = create_test_user()
    # Create a test portfolio
    portfolio = create_test_portfolio(user.id)
    # Create a test transaction associated with the portfolio
    transaction = Transaction(
        pair='BTC/USD',
        side='buy',
        price=50000,
        quantity=1,
        amount=50000,
        portfolio_id=portfolio.id
    )
    # Create a test position
    position = create_test_position(transaction, 'long')
    save_changes(position)
    transaction.position_id = position.id
    save_changes(transaction)
    # print("***** TEST ******")
    # print(f"Portfolio ID: {portfolio.id}")
    # print(f"Transaction ID: {transaction.id}")
    # print(f"Position ID: {position.id}")
    return portfolio, transaction

def create_test_portfolio_with_transactions():
    # Create a test user
    user = create_test_user()
    # Create a test portfolio
    portfolio = create_test_portfolio(user.id)

    # Create a test transaction associated with the portfolio
    transaction_buy = Transaction(
        #date=datetime.utcnow(),
        pair='BTC/USD',
        side='buy',
        price=50000,
        quantity=1,
        amount=50000,
        portfolio_id=portfolio.id
    )
    transaction_sell = Transaction(
        #date=datetime.utcnow(),
        pair='BTC/USD',
        side='sell',
        price=60000,
        quantity=1,
        amount=60000,
        portfolio_id=portfolio.id
    )
    # Create a test position
    position = create_test_position(transaction_buy, 'long')
    save_changes(position)
    transaction_buy.position_id = position.id
    save_changes(transaction_buy)
    transaction_sell.position_id = position.id
    save_changes(transaction_sell)
    transactions = [transaction_buy, transaction_sell]
    return portfolio, transactions

def save_changes(data):
    db.session.add(data)
    db.session.commit()