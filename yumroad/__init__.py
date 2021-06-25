from flask import Flask, render_template

from yumroad.blueprints.products import product_bp
from yumroad.blueprints.stores import store_bp
from yumroad.blueprints.users import user_bp
from yumroad.blueprints.checkout import checkout_bp

from yumroad.config import configurations
from yumroad.extensions import (csrf, db, migrate, mail, login_manager, checkout)
# We need this line for alembic to discover the models.
import yumroad.models


def create_app(environment_name='dev'):
    app = Flask(__name__)
    config = configurations[environment_name]
    app.config.from_object(config)
    db.init_app(app)
    csrf.init_app(app)
    # need render_as_batch to correctly generate migrations for sqlite
    migrate.init_app(app, db, render_as_batch=True)
    mail.init_app(app)
    login_manager.init_app(app)
    checkout.init_app(app)

    app.register_blueprint(product_bp)
    app.register_blueprint(store_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(checkout_bp)
    return app

# FLASK_DEBUG=true FLASK_APP="yumroad:create_app('dev')" flask run