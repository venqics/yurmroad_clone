import os
from decouple import config

folder_path = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('YUMROAD_SECRET_KEY')
    
    MAIL_SERVER= os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT= os.getenv('MAIL_PORT',587)
    MAIL_USERNAME= os.getenv('MAIL_USERNAME')
    MAIL_USE_TLS='True'
    MAIL_PASSWORD= os.getenv('MAIL_PASSWORD')
    
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'sk_test_51J4fpnSHO19FRh9CgjieC7ukn57c0tF3gPLTpMTJ7Xxpvepk6RvWCCxfY3MVaqWgs3WWLFavQhIZ1OzRMQyAKWFS00TYMevWWi')
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY','pk_test_51J4fpnSHO19FRh9CJ8LQ6VmINhBGlTQx4SAlocYvToJDZQa912oNJCqNNkFyJtj1jqTUWRs0IraeX8rWIUfa5h8h00dPWId8xt')
    STRIPE_WEBHOOK_KEY= 'whsec_dDaN58M6BzFkNobyQFmtx2Q8xMjNpmuf'
    SENTRY_DSN = "https://5e0c58f614924b7b8a0e33a221ba844f@o501456.ingest.sentry.io/5828526"

    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    RQ_REDIS_URL = REDIS_URL
    RQ_DASHBOARD_REDIS_URL = RQ_REDIS_URL

class DevConfig(BaseConfig):
    SECRET_KEY = os.getenv('YUMROAD_SECRET_KEY', '00000abcdef')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(folder_path, 'dev.db'))
    SQLALCHEMY_ECHO = True
    ASSETS_DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'

class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(folder_path, 'test.db'))
    SECRET_KEY = os.getenv('YUMROAD_SECRET_KEY', '12345abcdef')
    WTF_CSRF_ENABLED = False
    ASSETS_DEBUG = True
    RQ_ASYNC = False
    RQ_CONNECTION_CLASS = 'fakeredis.FakeStrictRedis'
    DEBUG_TB_ENABLED = False
    CACHE_TYPE = 'null'
    CACHE_NO_NULL_WARNING = True

class ProdConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = b"postgres://xzplizxlmbbpnl:ae03f6941b7bf0f64d61cc494b1d64b8119b"
    SESSION_PROTECTION = "strong"
    # You should be using HTTPS in production anyway, but if you are not, turn
    # these two off
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    ASSETS_DEBUG = False
    RQ_REDIS_URL = REDIS_URL = os.getenv('REDIS_URL')
    RQ_ASYNC = (REDIS_URL is not None)
    CACHE_TYPE = 'redis'
    CACHE_KEY_PREFIX = 'yumroad-'

configurations = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}
