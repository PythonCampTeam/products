import unittest
# from nameko.rpc import rpc, RpcProxy
from unittest.mock import MagicMock, patch
#from notifications import Notifications
# from rpc import products
# from nameko.testing.services import worker_factory
import stripe
from rpc.endpoints import Products, get_object
# from stripe.test.helper import StripeResourceTest


class Product_custom(unittest.TestCase):

    def setUp(self):
        self.id_product = "prod_BDQT7ifqt1FFc1"
        self.id_product2 = "prod_BDQT7ifqt1FFc1"
        self.id_sku = "sku_BDQTnZpwWglI3a"
        self.product = stripe.Product.retrieve("prod_BDQT7ifqt1FFc1")
        self.obj = Products()

    def test_handle_raises(self):
        '''Test for checking raises'''
        obj = self.obj
        id_product = self.id_product
        error_delete = 'Status is: 400, message is: The SKU you attempted to delete cannot be deleted because it is part of an order.'
        error_get = 'Status is: 404, message is: No such product: dad'
        self.assertEqual(obj.delete_product(id_product), error_delete)
        self.assertEqual(obj.get_product("dad"), error_get)

    # def test_update_raises(self):
    #     obj = self.obj
    #     body = {"id": "prod_BDQT7ifqt1FFc1",
    #             "Description": "Chappy is love!",
    #             "name": "Best Chappy"}
    #     error_update = 'Status is: 400, message is: Received unknown parameter: Description'
    #     self.assertEqual(obj.update_product(body), error_update)

    def test1(self):
        '''Test for checking raises'''
        obj = self.obj
        self.assertEqual(get_object("prod_BDQT7ifqt1FFc1"), self.product)
        self.assertEqual(obj.get_sku_product(self.id_product2),
                         self.id_sku)
        self.assertEqual(obj.get_product("prod_BDQT7ifqt1FFc1"),
                         self.product)

    # def test_update_product(self):
    #     '''Test for checking raises'''
    #     obj = self.obj
    #     product = stripe.Product.retrieve(self.id_product2)
    #     body = {"id": "prod_BCz7vruER4ugcJ",
    #             "description": "Chappy is love!",
    #             "name": "Best Chappy"}
    #     self.assertEqual(obj.update_product(body),
    #                      product)


if __name__ == '__main__':
    unittest.main()


# class ProductTest(StripeResourceTest):
#
#     def test_list_products(self):
#         stripe.Product.list()
#         self.requestor_mock.request.assert_called_with(
#             'get',
#             '/v1/products',
#             {}
#         )
#
#     def test_delete_products(self):
#         p = stripe.Product(id='product_to_delete')
#         p.delete()
#
#         self.requestor_mock.request.assert_called_with(
#             'delete',
#             '/v1/products/product_to_delete',
#             {},
#             None
#         )
#
#
# class SKUTest(StripeResourceTest):
#
#     def test_list_skus(self):
#         stripe.SKU.list()
#         self.requestor_mock.request.assert_called_with(
#             'get',
#             '/v1/skus',
#             {}
#         )
#
#     def test_delete_skus(self):
#         sku = stripe.SKU(id='sku_delete')
#         sku.delete()
#
#         self.requestor_mock.request.assert_called_with(
#             'delete',
#             '/v1/skus/sku_delete',
#             {},
#             None
#         )
#
#
# class OrderTest(StripeResourceTest):
#
#     def test_list_orders(self):
#         stripe.Order.list()
#         self.requestor_mock.request.assert_called_with(
#             'get',
#             '/v1/orders',
#             {}
#         )
#
#     def test_pay_order(self):
#         order = stripe.Order(id="or_pay")
#         order.pay()
#
#         self.requestor_mock.request.assert_called_with(
#             'post',
#             '/v1/orders/or_pay/pay',
#             {},
#             None
#         )
#
#     def test_return_order(self):
#         order = stripe.Order(id="or_return")
#         order.return_order()
#
#         self.requestor_mock.request.assert_called_with(
#             'post',
#             '/v1/orders/or_return/returns',
#             {},
#             None
#         )
