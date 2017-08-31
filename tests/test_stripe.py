import unittest
# from unittest.mock import MagicMock, patch
from unittest.mock import patch
import stripe
# from products.rpc.endpoints import Products, get_object
from products.rpc.endpoints import Products, get_object


class ProductsTest(unittest.TestCase):

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
        # self.sku = {
        #          'name': 'Test_sku',
        #          'object': 'sku',
        #          'inventory': {
        #              'quantity': 500,
        #              'type': 'finite'
        #          }
        #          }
        # self.sku_obj = stripe.StripeObject().construct_from(self.sku, '')
        self.product1 = stripe.StripeObject().construct_from(
                              self.items.get("data")[0], '')
        self.product2 = stripe.StripeObject().construct_from(
                              self.items.get("data")[1], '')
        self.sku_obj = self.product1.skus

    @patch('stripe.Product.retrieve')
    def test_get_sku(self, mock_poduct_retrieve):
        """Check method return id's sku of products"""
        mock_poduct_retrieve.return_value = self.product1
        print("Check get_sku_product")
        print(self.obj.get_sku_product(self.id_product))
        self.assertEqual(self.obj.get_sku_product(self.id_product), '222')
        self.assertTrue(mock_poduct_retrieve.called)

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
        mock_poduct_retrieve.return_value = self.product2
        mock_delete_sku.return_value = {"sku": "delete"}
        mock_delete_product.return_value = {"products": "delete"}
        print("Check delete products")
        self.assertTrue(mock_delete_sku is stripe.SKU.delete)
        self.assertTrue(mock_delete_product is stripe.Product.delete)
        self.assertTrue(stripe.Product.retrieve is mock_poduct_retrieve)
        self.assertTrue(stripe.SKU.retrieve is mock_sku_retrieve)
        print(self.obj.delete_product(self.id_product))
        self.assertEqual(self.obj.delete_product(self.id_product),
                         {"products": "delete"})

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
        print("Mock check create products")
        self.assertEqual(self.obj.create_product(body), self.product1)
        self.assertTrue(mock_product.called)
        self.assertTrue(mock_sku.called)

    @patch('stripe.Product.retrieve')
    def test_get_product(self, mock_get_product):
        mock_get_product.return_value = self.product1
        print("Mock check with retrieve")
        self.assertEqual(get_object(self.id_product), self.product1)
        self.assertTrue(mock_get_product.called)

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
        self.assertIsNotNone(error_dict.get("errors"))

    @patch('stripe.Product.save')
    @patch('stripe.Product.retrieve')
    def test_update_product(self, mock_poduct_retrieve, mock_product_update):
        mock_poduct_retrieve.return_value = self.product1
        mock_product_update.return_value = {"status": "product updated"}
        body = {"name": "super test",
                "description": "Oooooo",
                "skus": {"data": "Lol"}}
        print(self.obj.update_product(self.id_product, body))

    @patch('stripe.Product.save')
    @patch('stripe.Product.retrieve')
    def test_update_raises(self, mock_poduct_retrieve, mock_product_update):
        product = stripe.StripeObject().construct_from(self.items.get("data")[0], '')
        json_body = {'error': {'message': 'No such product: 4545',
                               'param': 'id',
                               'type': 'invalid_request_error'}}
        mock_poduct_retrieve.return_value = product
        mock_product_update.side_effect = stripe.error.InvalidRequestError(message="error!", param="id product", json_body=json_body)
        body = {"name": "super test",
                "description": "Oooooo",
                "skus": {"data": "Lol"}}
        print(self.obj.update_product(self.id_product, body))

    @patch('stripe.Product.list')
    def test_filter_product(self, mock_list_products):
        product = stripe.StripeObject().construct_from(self.items, '')
        mock_list_products.return_value = product
        print(self.obj.search_products(False, 'price', False))
        print(self.obj.search_products(False, 'price', False))
        print(self.obj.search_products('cats', 'price', False))
        print(self.obj.search_products('toys', 'price', False))


if __name__ == '__main__':
    unittest.main()
