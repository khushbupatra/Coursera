from factory import Faker, SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from service.models import db, Product

class ProductFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = db.session

    id = Faker('uuid4')
    name = Faker('word')
    description = Faker('text')
    price = Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    available = Faker('boolean')
    category = Faker('word')