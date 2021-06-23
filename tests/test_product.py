from flask import url_for
import pytest

from yumroad.models import db, Product, User

def create_product(name="Sherlock Homes", description="a house hunting real estate agent", user=None, store=None):
    user = user or User.create("owner@example.com", "test")
    product = Product(name="Sherlock Homes", description="a house hunting detective")
    db.session.add(product)
    db.session.commit()
    return product

# Unit Tests
def test_product_creation(client, init_database):
    assert Product.query.count() == 0
    create_product()
    assert Product.query.count() == 1

def test_name_validation(client, init_database):
    assert Product.query.count() == 0
    with pytest.raises(ValueError):
        Product(name="bad", description="should be an invalid name")
    assert Product.query.count() == 0

# Functional Tests
def test_index_page(client, init_database):
    product = create_product()
    response = client.get(url_for('product.index'))
    assert response.status_code == 200
    assert b'Yumroad' in response.data
    assert product.name in str(response.data)

    expected_link = url_for('product.details', product_id=product.id)
    assert expected_link in str(response.data)

def test_details_page(client, init_database):
    product = create_product()
    response = client.get(url_for('product.details', product_id=product.id))
    assert response.status_code == 200
    assert b'Yumroad' in response.data
    assert b'Purchase coming soon' in response.data
    assert product.name in str(response.data)

def test_unauthed_new_page(client, init_database):
    response = client.get(url_for('product.create'))
    assert response.status_code == 302

def test_new_page(client, init_database, authenticated_request):
    import flask
    print(flask.session)
    response = client.get(url_for('product.create'))

    assert response.status_code == 200
    assert b'Name' in response.data
    assert b'Create' in response.data

def test_creation(client, init_database, authenticated_request):
    response = client.post(url_for('product.create'),
                            data=dict(name='test product', description='is persisted'),
                            follow_redirects=True)

    assert response.status_code == 200
    assert b'test product' in response.data
    assert b'Purchase' in response.data

def test_invalid_creation(client, init_database, authenticated_request):
    response = client.post(url_for('product.create'),
                            data=dict(name='ab', description='is not valid'),
                            follow_redirects=True)

    assert response.status_code == 200
    assert b'is not valid' in response.data
    assert b'Field must be between' in response.data
    assert b'is-invalid' in response.data
