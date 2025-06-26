import unittest
from service import app
from service.models import db, Product
from tests.factories import ProductFactory

class TestProductRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_product(self):
        """Test getting a single product"""
        product = ProductFactory()
        response = self.app.get(f"/products/{product.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(product.name, response.get_data(as_text=True))

    def test_update_product(self):
        """Test updating a product"""
        product = ProductFactory()
        data = {"name": "Updated Name"}
        response = self.app.put(f"/products/{product.id}", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated Name", response.get_data(as_text=True))

    def test_delete_product(self):
        """Test deleting a product"""
        product = ProductFactory()
        response = self.app.delete(f"/products/{product.id}")
        self.assertEqual(response.status_code, 204)
        response = self.app.get(f"/products/{product.id}")
        self.assertEqual(response.status_code, 404)

    def test_list_all_products(self):
        """Test listing all products"""
        ProductFactory.create_batch(3)
        response = self.app.get("/products")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 3)

    def test_list_by_name(self):
        """Test listing products by name"""
        ProductFactory(name="Special Product")
        response = self.app.get("/products?name=Special Product")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data[0]["name"], "Special Product")

    def test_list_by_category(self):
        """Test listing products by category"""
        ProductFactory(category="Electronics")
        response = self.app.get("/products?category=Electronics")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data[0]["category"], "Electronics")

    def test_list_by_availability(self):
        """Test listing products by availability"""
        ProductFactory(available=True)
        response = self.app.get("/products?available=true")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data[0]["available"])