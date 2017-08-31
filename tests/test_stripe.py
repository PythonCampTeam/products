import unittest
from unittest.mock import patch

import stripe

from products.rpc.products import Products, get_object


class ProductsTest(unittest.TestCase):
    """Class for testing endpoints"""

    def setUp(self):
        self.id_product = "prod_BDQT7ifqt1FFc1"
        self.obj = Products()
        self.items = {"data": [{"name": "D", "description": "test1", "id": "1",
                               "metadata":
                                {"category": "food",
                                 "for": "cats",
                                 "type": "fish"},
                      "skus": {"data": [{"price": 1140,
                                         "id": "222",
                                         "inventory": {
                                              "quantity": 500,
                                              "type": "finite"
                                          }}]}
                       },
                      {"name": "W", "description": "test1", "id": "2",
                       "metadata":
                       {"category": "toys",
                        "for": "dogs",
                        "type": "ball"},
                       "skus": {"data": [{"price": 25,
                                          "id": "111",
                                          "inventory": {
                                              "quantity": 500,
                                              "type": "finite"
                                          }}]}
                       },
                       {"name": "A", "description": "test1", "id": "3",
                        "metadata":
                        {"category": "food",
                         "for": "cats",
                         "type": "fish"},
                        "skus": {"data": [{"price": 110,
                                           "id": "111",
                                           "inventory": {
                                            "quantity": 500,
                                            "type": "finite"
                                            }}]}
                        }
                       ]
                      }
        self.json_body = {'error': {'message': 'Testin exceptions',
                                    'param': 'id',
                                    'type': 'invalid_request_error'}}
        self.exp = stripe.error.InvalidRequestError(
                                                    message="Ooops",
                                                    param="id",
                                                    json_body=self.json_body,
                                                    http_status='400'
                                                    )
        self.product1 = stripe.StripeObject().construct_from(
                              self.items.get("data")[0], '')
        self.sku_obj = self.product1.skus

    @patch('stripe.Product.retrieve')
    def test_get_sku(self, mock_poduct_retrieve):
        """Check method return id's sku of products"""
        mock_poduct_retrieve.return_value = self.product1
        self.assertEqual(self.obj.get_sku_product(self.id_product), '222')
        self.assertTrue(mock_poduct_retrieve.called)
        print("Check get_sku_product")

    @patch('stripe.SKU.retrieve')
    @patch('stripe.Product.retrieve')
    @patch('stripe.Product.delete')
    @patch('stripe.SKU.delete')
    def test_delete_mock(self, mock_delete_sku, mock_delete_product,
                         mock_poduct_retrieve, mock_sku_retrieve):
        """"Check method delete product"""
        sku = {"object": "skus",
               "data": {"price": 50, "id": "111"},
               "inventory": {
                "type": "finite",
                "quantity": 500
               }}
        sku_obj = stripe.StripeObject().construct_from(sku, '')
        mock_sku_retrieve.return_value = sku_obj
        mock_poduct_retrieve.return_value = self.product1
        mock_delete_sku.return_value = {"sku": "delete"}
        mock_delete_product.return_value = {"products": "delete"}
        self.assertTrue(mock_delete_sku is stripe.SKU.delete)
        self.assertTrue(mock_delete_product is stripe.Product.delete)
        self.assertTrue(stripe.Product.retrieve is mock_poduct_retrieve)
        self.assertTrue(stripe.SKU.retrieve is mock_sku_retrieve)
        self.assertEqual(self.obj.delete_product(self.id_product),
                         {"products": "delete"})
        print("Check delete products")

    @patch('stripe.Product.retrieve')
    @patch('stripe.Product.create')
    @patch('stripe.SKU.create')
    def test_create_mock(self, mock_sku, mock_product, mock_poduct_retrieve):
        """Test for checking create product object and sku object"""
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

        product_create = stripe.StripeObject().construct_from(
                              response_product, '')
        mock_product.return_value = product_create
        mock_sku.return_value = self.sku_obj
        mock_poduct_retrieve.return_value = self.product1
        self.assertEqual(self.obj.create_product(body), self.product1)
        self.assertTrue(mock_product.called)
        self.assertTrue(mock_sku.called)
        print("Check create products")

    @patch('stripe.Product.retrieve')
    def test_get_product(self, mock_get_product):
        """Check methods get_product and get_object"""
        mock_get_product.return_value = self.product1
        self.assertEqual(get_object(self.id_product), self.product1)
        self.assertEqual(self.obj.get_product(self.id_product), self.product1)
        self.assertTrue(mock_get_product.called)
        print("Mock check with retrieve")

    def test_create_validate(self):
        """Check validate parameters for method of create_product"""
        obj = self.obj
        body = {}
        error_dict = obj.create_product(body)
        self.assertIsNotNone(error_dict.get("errors"))
        print('Check validate')

    @patch('stripe.Product.save')
    @patch('stripe.Product.retrieve')
    def test_update_product(self, mock_poduct_retrieve, mock_product_update):
        """Ckeck method update_product"""
        mock_poduct_retrieve.return_value = self.product1
        mock_product_update.return_value = {"status": "product updated"}
        body = {"name": "super test",
                "description": "Oooooo",
                "skus": {"data": "Lol"}}
        self.assertEqual(self.obj.update_product(self.id_product, body),
                         {"status": "product updated"})
        print('Check update_product ')

    @patch('stripe.Product.list')
    def test_filter_product(self, mock_list_products):
        """Ckeck method search_products and sorted"""
        product = stripe.StripeObject().construct_from(self.items, '')
        mock_list_products.return_value = product
        self.assertIsNotNone(self.obj.search_products(False, 'price', False))
        self.assertIsNotNone(self.obj.search_products(False, 'price', False))
        self.assertIsNotNone(self.obj.search_products('cats', 'name', False))
        self.assertIsNotNone(self.obj.search_products('toys',
                             'category', False))
        self.assertTrue(mock_list_products.called)
        print('Check filter_product')

    @patch('stripe.Product.save')
    @patch('stripe.Product.retrieve')
    def test_update_raises(self, mock_poduct_retrieve, mock_product_update):
        """Check call raise in method update_product"""
        mock_poduct_retrieve.return_value = self.product1
        mock_product_update.side_effect = self.exp
        body = {"name": "super test",
                "description": "Oooooo",
                "skus": {"data": "Lol"}}
        raise_exp = self.obj.update_product(self.id_product, body)
        self.assertTrue('Status is: 400' in raise_exp)
        self.assertTrue(mock_product_update.called)
        print("Check called raise in update product")

    @patch('stripe.Product.retrieve')
    def test_delete_raise(self, mock_poduct_retrieve):
        """"Check called raise in method delete product and get product"""
        mock_poduct_retrieve.side_effect = self.exp
        self.assertTrue(stripe.Product.retrieve is mock_poduct_retrieve)
        raise_exp_delete = self.obj.delete_product(self.id_product)
        self.assertTrue('Testin exceptions' in raise_exp_delete)
        raise_exp_get_product = self.obj.get_product(self.id_product)
        self.assertTrue('Testin exceptions' in raise_exp_get_product)
        self.assertTrue(mock_poduct_retrieve.called)
        print("Check called raise in delete product and get product")


if __name__ == '__main__':
    unittest.main()
