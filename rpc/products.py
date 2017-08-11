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
        item = stripe.Product.retrieve(ID)
        return item

    @rpc
    def create_product(self, name, description,
                       attributes, package_dimensions):
        stripe.api_key = "sk_test_K5QUkUgvUNKvDD9fEGYBI6Gi"
        # name = kwargs.get('name')
        # description = kwargs.get('description')
        # attributes = kwargs.get('attributes')
        # package_dimensions = kwargs.get('package_dimensions')
        item = stripe.Product.create(
         name=name,
         description=description,
         attributes=attributes,
         package_dimensions=package_dimensions
         )
        return item

    @rpc
    def list_products(self, count=100):
        item = stripe.Product.list(limit=count)
        return item

    @rpc
    def delete_product(self, ID):
        product = stripe.Product.retrieve(ID)
        res = product.delete()
        return res

    @rpc
    def update_product(self, ID, KEY, VALUE):
        product = stripe.Product.retrieve(ID)
        product.metadata[KEY] = VALUE
        product.save()
