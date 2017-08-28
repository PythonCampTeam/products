import unittest
# from nameko.rpc import rpc, RpcProxy
from unittest.mock import MagicMock, patch
import stripe
# from products.rpc.endpoints import Products

from rpc.endpoints import Products


class ProductsTest(unittest.TestCase):

    def setUp(self):
        self.id_product = "prod_BDQT7ifqt1FFc1"
        self.id_sku = "sku_BDQTnZpwWglI3a"
        self.product = stripe.Product.retrieve("prod_BDQT7ifqt1FFc1")
        self.obj = Products()

    def test_mock_sort(self):
        """Test for checking sort product"""
        obj = Products()
        obj.search_products = MagicMock(return_value='200')
        self.assertEqual(obj.search_products(False, 'name', True), '200')
        print("Mock sort check")
        self.assertTrue(obj.search_products.called)

    @patch('products.rpc.endpoints.Products.create_product',
           return_value='202')
    def test_create_mock(self, create_product):
        """Mocking create product and delete product"""
        body = {
                "name": "Test",
                "description": "Testing",
                "attributes": ["manufacturer",
                               "material"],
                "package_dimensions":  {"height": 5.0, "length": 5.0,
                                        "weight": 5.0, "width": 5.0},
                "metadata": {
                 "category": "food",
                 "for": "cats",
                 "type": "fish"
                },
                "attributes_sku": {
                 "manufacturer": "PetHappy",
                 "material": "rubber"},
                "price": 50,
                "inventory": {
                 "type": "finite",
                 "quantity": 500
                }
            }
        res = create_product(body)
        print(res)
        self.assertEqual(res, '202')
        assert create_product.called
        print("Mock check")

    def test_create_delete(self):
        '''Test for checking create product and delete product'''
        obj = self.obj
        body = {
                "name": "Test",
                "description": "Testing",
                "attributes": ["manufacturer",
                               "material"],
                "package_dimensions":  {"height": 5.0, "length": 5.0,
                                        "weight": 5.0, "width": 5.0},
                "metadata": {
                 "category": "food",
                 "for": "cats",
                 "type": "fish"
                },
                "attributes_sku": {
                 "manufacturer": "PetHappy",
                 "material": "rubber"},
                "price": 50,
                "inventory": {
                 "type": "finite",
                 "quantity": 500
                }
            }
        product_test = obj.create_product(body)
        self.assertIsInstance(product_test, stripe.resource.Product)
        self.assertIsInstance(obj.delete_product(product_test.id),
                              stripe.resource.Product)

    def test_handle_raises(self):
        '''Test for checking raises in delete product and get product'''
        obj = self.obj
        id_product = self.id_product
        result_delete = obj.delete_product(id_product)

        # trying get not exist product
        result_get = obj.get_product("dad")
        print(result_delete, result_get)
        self.assertTrue('Status is: 400' in result_delete)
        self.assertTrue('Status is: 404' in result_get)

    def test_update_raises(self):
        """Test for checking raises in update product"""
        obj = self.obj
        id_product = "prod_BDQT7ifqt1FFc1"
        body = {
                "Description": "Chappy is love!",
                "name": "Best Chappy"
                }
        result = obj.update_product(id_product, body)
        self.assertTrue('Received unknown parameter: Description' in result)

    def test1(self):
        '''Test for checking update'''
        obj = self.obj
        self.assertEqual(obj.get_sku_product(self.id_product),
                         self.id_sku)
        self.assertEqual(obj.get_product(self.id_product),
                         self.product)

    def test_update_product(self):
        '''Test for checking raises update product'''
        obj = self.obj
        product = stripe.Product.retrieve("prod_BDQT7ifqt1FFc1")
        id_product = "prod_BDQT7ifqt1FFc1"
        body = {
                "description": "Chappy is love!",
                "name": "Best Chappy"
                }
        self.assertEqual(obj.update_product(id_product, body),
                         product)

    def test_filtering_product(self):
        '''Test for filtering products'''
        obj = self.obj
        result = obj.search_products("toys", "name", False)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
