from nameko.rpc import rpc


class Products(object):
    """ this class make Products request to add cost to trash
    Args:
        name(str): The name  tovar
        aditional(dict): information about tovar
    Return:
        cost(int): PPPPPP
        """
    name = 'ProductsRPC'

    @rpc
    def getproduct(self, **kwargs):
        doc_class = self.__dict__
        return {self.__class__.__name__: doc_class,
                'docs': self.__class__.__doc__}
