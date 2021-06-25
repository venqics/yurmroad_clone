from flask import url_for
import pytest
import vcr

from yumroad.models import db, Product

def create_book(name="Sherlock Homes", description="a house hunting real estate agent"):
    book = Product(name="Sherlock Homes", description="a house hunting detective", price_cents=500)
    db.session.add(book)
    db.session.commit()
    return book

# Unit Tests
def test_product_creation(client, init_database):
    assert Product.query.count() == 0
    create_book()
    assert Product.query.count() == 1

def test_name_validation(client, init_database):
    assert Product.query.count() == 0
    with pytest.raises(ValueError):
        Product(name="bad", description="should be an invalid name")
    assert Product.query.count() == 0

# Functional Tests
def test_index_page(client, init_database):
    book = create_book()
    response = client.get(url_for('product.index'))
    assert response.status_code == 200
    assert b'Yumroad' in response.data
    assert book.name in str(response.data)

    expected_link = url_for('product.details', product_id=book.id)
    assert expected_link in str(response.data)

@vcr.use_cassette('tests/cassettes/new_stripe_session.yaml',
                  filter_headers=['authorization'], record_mode='once')
def test_details_page(client, init_database):
    book = create_book()
    response = client.get(url_for('product.details', product_id=book.id))
    assert response.status_code == 200
    assert b'Yumroad' in response.data
    assert b'Buy for $5.00' in response.data
    assert book.name in str(response.data)

def test_non_existant_book(client, init_database):
    book = create_book()
    response = client.get(url_for('product.details', product_id=book.id+1))
    assert response.status_code == 404

def test_new_page_unauthorized(client, init_database):
    response = client.get(url_for('product.create'))
    assert response.status_code == 302

def test_new_page(client, init_database, authenticated_request):
    response = client.get(url_for('product.create'))

    assert response.status_code == 200
    assert b'Name' in response.data
    assert b'Create' in response.data

@vcr.use_cassette('tests/cassettes/new_stripe_session.yaml',
                  filter_headers=['authorization'], record_mode='once')
def test_creation(client, init_database, authenticated_request):
    response = client.post(url_for('product.create'),
                            data=dict(name='test product', description='is persisted', price=5),
                            follow_redirects=True)

    assert response.status_code == 200
    assert b'test product' in response.data
    assert b'Buy for $5.00' in response.data

def test_creation_without_price(client, init_database, authenticated_request):
    response = client.post(url_for('product.create'),
                            data=dict(name='test product', description='is persisted'),
                            follow_redirects=True)

    assert response.status_code == 200
    assert b'test product' in response.data
    assert b'Sold out' in response.data

def test_invalid_creation(client, init_database, authenticated_request):
    response = client.post(url_for('product.create'),
                            data=dict(name='ab', description='is not valid'),
                            follow_redirects=True)

    assert response.status_code == 200
    assert b'is not valid' in response.data
    assert b'Field must be between' in response.data
    assert b'is-invalid' in response.data

@vcr.use_cassette('tests/cassettes/new_stripe_session.yaml',
                  filter_headers=['authorization'], record_mode='once')
def test_post_checkout_success_page(client, init_database, user_with_product):
    product = Product.query.first()
    response = client.get(url_for('product.post_checkout', product_id=product.id,
                                  status='success', session_id='test_1'), follow_redirects=True)

    assert response.status_code == 200
    assert b'You will receive an email shortly' in response.data

@vcr.use_cassette('tests/cassettes/new_stripe_session.yaml',
                  filter_headers=['authorization'], record_mode='once')
def test_post_checkout_fail_page(client, init_database, user_with_product):
    product = Product.query.first()
    response = client.get(url_for('product.post_checkout', product_id=product.id,
                                  status='cancel', session_id='test_1'), follow_redirects=True)

    assert response.status_code == 200
    assert b'There was an error while attempting' in response.data
