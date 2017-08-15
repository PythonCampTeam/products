from nameko.rpc import rpc
import stripe
import operator


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
    def create_product(self, convert):
        """Creted a new product whith SKU object
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
            inventory (hash) Description of the SKU’s inventory.
        Returns:
            Returns a product object if the call succeeded.
            """
        name = convert.get("name")
        description = convert.get("description")
        attributes = convert.get("attributes")
        package_dimensions = convert.get("package_dimensions")
        metadata = convert.get("metadata")
        attributes_sku = convert.get("attributes_sku")
        price = convert.get("price")
        inventory = convert.get("inventory")
        item = stripe.Product.create(
            name=name,
            description=description,
            attributes=attributes,
            package_dimensions=package_dimensions,
            metadata=metadata
         )
        stripe.SKU.create(
            product=item.id,
            attributes=attributes_sku,
            price=price,
            package_dimensions=package_dimensions,
            currency="usd",
            inventory=inventory
        )

        return stripe.Product.retrieve(item.id)

    @rpc
    def list_products(self, count=100):
        """Return list products (max 100 items)
        Args:
            count(int) A limit on the number of objects to be returned.
                       The default is 100 items.
            item (list) Returns a list of products objects if the call succeeded
            """
        item = stripe.Product.list(limit=count)
        return item

    @rpc
    def delete_product(self, ID):
        """Delete a product.
        Args:
            ID (string) The ID of the product to delete.
        Returns:
            result (object) Returns an object with a deleted parameter on success.
            Otherwise, this call raises an error.
        """
        product = stripe.Product.retrieve(ID)
        result = product.delete()
        return result

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
            result (object) Returns the product object if the update succeeded.
        """
        product = stripe.Product.retrieve(id_product)
        product[key] = value
        result = product.save()
        return result

    @rpc
    def filter_products(self, category, order_by, DESC):
        """Returns the filtering product list
        Args:
            category (stripe) parameter for search
            items (list) List of all products
            order_by (str) parameter for to ordering
            DESC (bool) sorting direction
            result (list) list products sorting by category
        Returns
            sort (list) sorted list products"""
        items = stripe.Product.list(limit=100)["data"]
        result = [it for it in items if it.metadata.get("category")
                  == category]
        if order_by == "None" or order_by == "null":
            return result
        sort = Products.sorted(result, order_by, DESC)
        return sort

    @rpc
    def search_products(self, search, order_by, DESC):
        """Returns a list of products with a given parameter
        Args:
            search (string) parameter for search
            items (list) List of all products
            order_by (string) parameter for to ordering
            DESC (bool) sorting direction
            result (list) list products sorting by search
        Returns
            result (list) sorted list products"""
        items = stripe.Product.list(limit=100)["data"]
        result = [it for it in items if it.get("name") == search or
                  it.metadata.get("type") == search or
                  it.metadata.get("category") == search or
                  it.metadata.get("for") == search]
        if order_by == "None" or order_by == "null":
            return result
        sort = Products.sorted(result, order_by, DESC)
        return sort

    @rpc
    def sorted_products(self, sorty_value, DESC):
        """Returns the sorted ordered list
        Args:
            items (list) List of all products
            sorty_value (string) parameter for to ordering
            DESC (bool) sorting direction
        Return:
            sort (list) list products ordered"""
        items = stripe.Product.list(limit=100)["data"]
        sort = Products.sorted(items, sorty_value, DESC)
        return sort

    def sorted(items, sorty_value, DESC):
        """Returns the sorted product list
        Args:
            sorty_value (str) parameter for to sorting
            items (list) List of objects products
            prod_sorted (list) sorted products list
            func_sort (func) Function for sorting
            DESC (bool) sorting direction
        Returns:
            Sorted products list"""
        def sorty_price(item):
            """Function for sort by price"""
            return item.skus.data[0].price
        if sorty_value == "price":
            func_sort = sorty_price
            return sorted(items, key=func_sort, reverse=DESC)
        if items[0].get(sorty_value) is None:
            func_sort = operator.attrgetter('metadata.'+sorty_value)
            return sorted(items, key=func_sort, reverse=DESC)
        func_sort = operator.attrgetter(sorty_value)
        return sorted(items, key=func_sort, reverse=DESC)
