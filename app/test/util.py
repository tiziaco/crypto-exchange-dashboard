from app.main.models.user import User
from app.main.models.portfolio import Portfolio, Transaction
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

def create_test_portfolio_with_transaction():
    # Create a test user
    user = create_test_user()
    # Create a test portfolio
    portfolio = create_test_portfolio(user.id)

    # Create a test transaction associated with the portfolio
    transaction = Transaction(
        #date=datetime.utcnow(),
        pair='BTC/USD',
        side='buy',
        price=50000,
        quantity=1,
        amount=50000,
        portfolio_id=portfolio.id
    )
    save_changes(transaction)
    return portfolio, transaction

def create_test_portfolio_with_transactions():
    # Create a test user
    user = create_test_user()
    # Create a test portfolio
    portfolio = create_test_portfolio(user.id)

    # Create a test transaction associated with the portfolio
    transaction1 = Transaction(
        #date=datetime.utcnow(),
        pair='BTC/USD',
        side='buy',
        price=50000,
        quantity=1,
        amount=50000,
        portfolio_id=portfolio.id
    )
    transaction2 = Transaction(
        #date=datetime.utcnow(),
        pair='BTC/USD',
        side='sell',
        price=60000,
        quantity=1,
        amount=60000,
        portfolio_id=portfolio.id
    )
    save_changes(transaction1)
    save_changes(transaction2)
    transactions = [transaction1, transaction2]
    return portfolio, transactions

def save_changes(data):
    db.session.add(data)
    db.session.commit()