import unittest
from service.models import Product, db
from service import app
from tests.factories import ProductFactory

class TestProductModels(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_product(self):
        """Test creating a product"""
        product = ProductFactory()
        self.assertIsNotNone(product.id)
        self.assertIsNotNone(product.name)
        self.assertIsNotNone(product.description)

    def test_find_product(self):
        """Test finding a product by ID"""
        product = ProductFactory()
        found = Product.find(product.id)
        self.assertEqual(found.id, product.id)

    def test_update_product(self):
        """Test updating a product"""
        product = ProductFactory()
        original_name = product.name
        product.name = "Updated Name"
        product.update()
        updated = Product.find(product.id)
        self.assertEqual(updated.name, "Updated Name")
        self.assertNotEqual(updated.name, original_name)

    def test_delete_product(self):
        """Test deleting a product"""
        product = ProductFactory()
        product.delete()
        found = Product.find(product.id)
        self.assertIsNone(found)

    def test_list_all_products(self):
        """Test listing all products"""
        ProductFactory.create_batch(5)
        products = Product.all()
        self.assertEqual(len(products), 5)

    def test_find_by_name(self):
        """Test finding products by name"""
        ProductFactory(name="Special Product")
        products = Product.find_by_name("Special Product")
        self.assertEqual(products[0].name, "Special Product")

    def test_find_by_category(self):
        """Test finding products by category"""
        ProductFactory(category="Electronics")
        products = Product.find_by_category("Electronics")
        self.assertEqual(products[0].category, "Electronics")

    def test_find_by_availability(self):
        """Test finding products by availability"""
        ProductFactory(available=True)
        products = Product.find_by_availability(True)
        self.assertTrue(products[0].available)