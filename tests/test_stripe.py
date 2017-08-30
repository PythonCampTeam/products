import unittest
from unittest.mock import MagicMock, patch
import stripe
from products.rpc.endpoints import Products, get_object


class ProductsTest(unittest.TestCase):

    def setUp(self):
        self.id_product = "prod_BDQT7ifqt1FFc1"
        self.id_sku = "sku_BDQTnZpwWglI3a"
        self.product = stripe.Product.retrieve("prod_BDQT7ifqt1FFc1")
        self.obj = Products()
        self.items = [{"name": "A", "description": "test1", "id": "1",
                       "metadata":
                       {"category": "food",
                        "for": "cats",
                        "type": "fish"},
                      "skus": {"data":
                               [{"price": 50, "id": "222"}]}
                       },
                      {"name": "A", "description": "test1", "id": "1",
                       "metadata":
                       {"category": "food",
                        "for": "cats",
                        "type": "fish"},
                      "skus": {"data":
                               [{"price": 50, "id": "111"}]}
                       }
                      ]
    def test_delete_mock(delf):
        pass

    @patch('stripe.Product.create')
    @patch('stripe.SKU.create')
    def test_create_mock(self, mock_sku, mock_product):
        """Test for checking create product and delete product"""
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

        response_product = {
                 'id': '1212',
                 'name': 'Test',
                 'object': 'product',
                 'description': 'Testing',
                 'metadata': {
                     'category': 'food',
                     'type': 'fish'
                 }
                 }
        response_sku = {
                 'name': 'Test_sku',
                 'object': 'sku',
                 'inventory': {
                     'quantity': 500,
                     'type': 'finite'
                 }
                 }
        mock_product.return_value = response_product
        mock_sku.return_value = response_sku
        # print(stripe.Product.create(body_prod))
        # print(stripe.SKU.create(body_sku))
        print(mock_product())
        print(mock_sku())
        print(self.obj.create_product(body))
        print(mock_product.called)
        print(mock_sku.called)
        print("Mock check with patch")

    @patch('stripe.Product.retrieve')
    def test_get_product(self, mock_get_product):
        response_product = {
                 'id': '1212',
                 'name': 'Test_mock_retrieve',
                 'object': 'product',
                 'description': 'Testing',
                 'metadata': {
                     'category': 'food',
                     'type': 'fish'
                 }
                 }
        mock_get_product.return_value = response_product
        print("Mock check with retrieve")
        # print(mock_get_product("prod_BDQT7ifqt1FFc1"))
        print(self.obj.get_product("prod_BDQT7ifqt1FFc1"))
        print(get_object("prod_BDQT7ifqt1FFc1"))
        print(mock_get_product.called)

    def test_create_validate(self):
        obj = self.obj
        body = {
                "name": "Test",
                "description": "Testing",
                "attributes": ["manufacturer",
                               "material"],
                "package_dimensions":  {},
            }
        error_dict = obj.create_product(body)
        print(error_dict)
        self.assertIsNotNone(error_dict.get("errors"))

    # def test_create_delete(self):
    #     '''Test for checking create product and delete product'''
    #     obj = self.obj
    #     body = {
    #             "name": "Test",
    #             "description": "Testing",
    #             "attributes": ["manufacturer",
    #                            "material"],
    #             "package_dimensions":  {"height": 5.0, "length": 5.0,
    #                                     "weight": 5.0, "width": 5.0},
    #             "metadata": {
    #              "category": "food",
    #              "for": "cats",
    #              "type": "fish"
    #             },
    #             "attributes_sku": {
    #              "manufacturer": "PetHappy",
    #              "material": "rubber"},
    #             "price": 50,
    #             "inventory": {
    #              "type": "finite",
    #              "quantity": 500
    #             }
    #         }
    #     product_test = obj.create_product(body)
    #     self.assertIsInstance(product_test, stripe.resource.Product)
    #     self.assertIsInstance(obj.delete_product(product_test.id),
    #                           stripe.resource.Product)
    #
    # def test_handle_raises(self):
    #     '''Test for checking raises in delete product and get product'''
    #     obj = self.obj
    #     id_product = self.id_product
    #     result_delete = obj.delete_product(id_product)
    #
    #     # trying get not exist product
    #     result_get = obj.get_product("dad")
    #     print(result_delete, result_get)
    #     self.assertTrue('Status is: 400' in result_delete)
    #     self.assertTrue('Status is: 404' in result_get)
    #
    # def test_update_raises(self):
    #     """Test for checking raises in update product"""
    #     obj = self.obj
    #     id_product = "prod_BDQT7ifqt1FFc1"
    #     body = {
    #             "Description": "Chappy is love!",
    #             "name": "Best Chappy"
    #             }
    #     result = obj.update_product(id_product, body)
    #     self.assertTrue('Received unknown parameter: Description' in result)
    #
    # def test1(self):
    #     '''Test for checking update'''
    #     obj = self.obj
    #     self.assertEqual(obj.get_sku_product(self.id_product),
    #                      self.id_sku)
    #     self.assertEqual(obj.get_product(self.id_product),
    #                      self.product)
    #
    # def test_update_product(self):
    #     '''Test for checking raises update product'''
    #     obj = self.obj
    #     product = stripe.Product.retrieve("prod_BDQT7ifqt1FFc1")
    #     id_product = "prod_BDQT7ifqt1FFc1"
    #     body = {
    #             "description": "Chappy is love!",
    #             "name": "Best Chappy"
    #             }
    #     self.assertEqual(obj.update_product(id_product, body),
    #                      product)
    #
    # def test_filtering_product(self):
    #     '''Test for filtering products'''
    #     obj = self.obj
    #     result1 = obj.search_products("toys", "name", False)
    #     self.assertIsNotNone(result1)


if __name__ == '__main__':
    unittest.main()
