from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from yumroad.payments import Checkout
from flask_assets import Environment
from flask_rq2 import RQ
from flask_debugtoolbar import DebugToolbarExtension
from flask_caching import Cache
from sqlalchemy import MetaData


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
mail = Mail()
assets_env = Environment()
checkout = Checkout()
rq2 = RQ()
debug_toolbar = DebugToolbarExtension()
cache = Cache()

#@rq2.job
#def average(x, y):
#   print("I am running")
#   return (x + y)/2