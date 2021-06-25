from yumroad import create_app, db
from yumroad.models import Product, Store, User

app = create_app('dev')

def reset():
    with app.app_context():
        db.drop_all()
        setup()

def setup():
    with app.app_context():
        db.create_all()
        user = User.create("test@example.com", "test")
        db.session.add(user)
        store = Store(name="The newline store", user=user)
        for i in range(2):
            prod = Product(name='Fullstack Book v{}'.format((1+i)*2),
                           description='Book #{} in the series'.format(i+1),
                           price_cents=100*i+1,
                           store=store)
            db.session.add(prod)
        db.session.commit()
