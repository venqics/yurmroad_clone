from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from yumroad.forms import ProductForm
from yumroad.models import Product, db

product_bp = Blueprint('product', __name__)

@product_bp.route('/')
def index():
    all_products = Product.query.all()
    return render_template('products/index.html', products=all_products)

@product_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, description=form.description.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('.details', product_id=product.id))
    return render_template('products/new.html', form=form)

@product_bp.route('/<product_id>')
def details(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('products/details.html', product=product)
