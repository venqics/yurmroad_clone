from flask import Flask, render_template

from yumroad.blueprints.products import product_bp
from yumroad.blueprints.users import user_bp
from yumroad.config import configurations
from yumroad.extensions import (csrf, db, login_manager)
# We need this line for alembic to discover the models.
import yumroad.models

def create_app(environment_name='dev'):
    app = Flask(__name__)
    config = configurations[environment_name]
    app.config.from_object(config)
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(product_bp)
    app.register_blueprint(user_bp)
    return app

# FLASK_DEBUG=true FLASK_APP="yumroad:create_app('dev')" flask run