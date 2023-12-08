import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))
# Load configuration from JSON file
print(basedir)
with open('keys.json', 'r') as keys_file:
    keys_data = json.load(keys_file)

class Config:
	"""Flask configuration variables."""

	# General Config
	APP_NAME = "Crypto Exchange Dashboard"
	DEBUG = True
	SECRET_KEYS = keys_data.get('SECRET_KEYS', {})

class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:1234@localhost:5432/portfolio_dashboard'
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

keys = Config.SECRET_KEYS

# TEST => OK
# # Access individual keys
# binance_api_key = keys.get('binance', {}).get('API_KEY')
# binance_api_secret = keys.get('binance', {}).get('API_SECRET')

# # Use the values as needed
# print(f"Binance API Key: {binance_api_key}")
# print(f"Binance API Secret: {binance_api_secret}")