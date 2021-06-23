from flask import Blueprint, render_template, redirect, request, url_for, abort
from flask_login import current_user, login_required

from yumroad.models import Product, db
from yumroad.forms import ProductForm

product_bp = Blueprint('product', __name__)

@product_bp.route('/')
def index():
    products = Product.query.all()
    return render_template('products/index.html', products=products)

@product_bp.route('/product/new', methods=['GET', 'POST'])
@login_required
def create():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data,
                        description=form.description.data,
                        creator=current_user,
                        store=current_user.store)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('product.details', product_id=product.id))
    return render_template('products/new.html', form=form)


@product_bp.route('/product/<product_id>')
def details(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('products/details.html', product=product)
