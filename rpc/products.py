from nameko.rpc import rpc
import stripe


class Products(object):
    """ This class created Products and retrieve list of products,
    delete product, update product, add product
    Note: See https://stripe.com"""
    name = 'ProductsRPC'

    stripe.api_key = "sk_test_K5QUkUgvUNKvDD9fEGYBI6Gi"

    @rpc
    def testing(self, **kwargs):
        """Check for work"""
        doc_class = self.__dict__
        return {self.__class__.__name__: doc_class,
                'docs': self.__class__.__doc__}

    @rpc
    def getproduct(self, id_product):
        """Return product on Id
        Args:
            ID (syring) The identifier for the product
        Returns:
            Returns a product object if the call succeeded."""
        item = stripe.Product.retrieve(id_product)
        return item

    @rpc
    def create_product(self, name, description,
                       attributes, package_dimensions, metadata):
        """Creted a new product
        Args:
            name (string) The product’s name, for the customer.
            description (string) The product’s description for the customer.
            attributes (lost of strings) A list of up to 5 attributes that each
                                         SKU can provide values for
            package_dimensions (hash) The dimensions of this product for
                                      shipping purposes:
                height (decimal) Height, in inches.
                length (decimal) Length, in inches.
                length (decimal) Length, in inches.
                weight (decimal) Weight, in ounces.
                width (decimal) Width, in inches.
            metadata (hash) Set of key/value pairs that you can attach to
                            an object. Use as category
        Returns:
            Returns a product object if the call succeeded.
            """
        item = stripe.Product.create(
         name=name,
         description=description,
         attributes=attributes,
         package_dimensions=package_dimensions,
         metadata=metadata
         )
        return item

    @rpc
    def list_products(self, count=100):
        """Return list products (max 100 item)
        Args:
            count(int) A limit on the number of objects to be returned.
                       The default is 100 items.
            Returns a list of products objects if the call succeeded"""
        item = stripe.Product.list(limit=count)
        return item

    @rpc
    def delete_product(self, ID):
        """Delete a product.
        Args:
            ID (string) The ID of the product to delete.
        Returns:
            Returns an object with a deleted parameter on success.
            Otherwise, this call raises an error.
        """
        product = stripe.Product.retrieve(ID)
        res = product.delete()
        return res

    @rpc
    def update_product(self, id_product, key, value):
        """Updates the specific product by setting the values of the parameters
           passed.
        Note: Note that a product’s attributes are not editable.
        Args:
            id_product (string) The ID of the product to update.
            key (string) The parameter to update.
            value New value for the parameter
        Returns:
            Returns the product object if the update succeeded.
        """
        product = stripe.Product.retrieve(id_product)
        product[key] = value
        res = product.save()
        return res
