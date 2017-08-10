from nameko.rpc import rpc
import stripe


class Products(object):
    """ this class make Products request to add cost to trash
    Args:
        name(str): The name  tovar
        aditional(dict): information about tovar
    Return:
        cost(int): PPPPPP
        """
    name = 'ProductsRPC'

    stripe.api_key = "sk_test_K5QUkUgvUNKvDD9fEGYBI6Gi"

    @rpc
    def testing(self, **kwargs):
        doc_class = self.__dict__
        return {self.__class__.__name__: doc_class,
                'docs': self.__class__.__doc__}

    @rpc
    def getproduct(self, ID):
        stripe.api_key = "sk_test_K5QUkUgvUNKvDD9fEGYBI6Gi"
        item = stripe.Product.retrieve(ID)
        return item
