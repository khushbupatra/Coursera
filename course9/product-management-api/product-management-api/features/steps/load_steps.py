from behave import fixture, use_fixture
from service import app, db
from service.models import Product

@fixture
def flask_client(context, *args, **kwargs):
    app.testing = True
    context.client = app.test_client()
    with app.app_context():
        db.create_all()
    yield context.client
    with app.app_context():
        db.drop_all()

def before_scenario(context, scenario):
    use_fixture(flask_client, context)