import pytest
from flask import url_for
from flask_login import login_user

from yumroad import create_app
from yumroad.models import db, User, Store, Product
from yumroad.extensions import login_manager, mail

@pytest.fixture
def app():
    app = create_app('test')
    yield app

@pytest.fixture
def init_database():
    db.create_all()
    yield db
    db.drop_all()

# TODO: actually just yield user, rename to logged_in_user
@pytest.fixture
def authenticated_request(client):
    new_user = User.create("test@example.com", "pass")
    store = Store(name="Test Store", user=new_user)
    db.session.add(store)
    db.session.commit()

    response = client.post(url_for('user.login'), data={
        'email': "test@example.com",
        'password': "pass"
    }, follow_redirects=True)
    yield new_user


@pytest.fixture
def mail_outbox():
    with mail.record_messages() as outbox:
        yield outbox

@pytest.fixture
def app_context(app):
    with app.app_context() as ctx:
        yield ctx

@pytest.fixture
def user_with_product():
    new_user = User.create("test@example.com", "pass")
    store = Store(name="Test Store", user=new_user)
    product = Product(name='Test Product', description='a product', store=store)
    db.session.add(product)
    db.session.commit()
    yield new_user
