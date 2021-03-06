import operator

import cerberus
import stripe
from nameko.rpc import rpc

from products.config.settings.common.security import key
from products.rpc.exceptions import handling
from products.rpc.validate import schema_product

Validator = cerberus.Validator
schema = schema_product


def get_object(id_product):
    """Private method retutn product object by id"""
    return stripe.Product.retrieve(id_product)


class Products(object):
    """ This class created Products and retrieve list of products,
        delete product, update product, add product.

    Note: See https://stripe.com

    """
    name = 'Productsrpc'

    stripe.api_key = key

    @rpc
    def get_sku_product(self, id_product):
        product = get_object(id_product)
        return product.skus.data[0].id

    @rpc
    def get_product(self, id_product):
        """Return product on Id

        Args:
            id_product (syring) The identifier for the product

        Returns:
            Returns a product object if the call succeeded.
            Otherwise, this call raises an error.

        """
        try:
            item = get_object(id_product)
        except stripe.error.InvalidRequestError as e:
            return handling(e)
        return item

    @rpc
    def create_product(self, body):
        """Creted a new product whith SKU object

        Args:
            name (string) The product’s name, for the customer.
            description (string) The product’s description for the customer.
            attributes (list of strings) A list of up to 5 attributes that each
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
        v = Validator()
        if not v.validate(body, schema):
            return {"errors": v.errors}
        name = body.get("name")
        description = body.get("description")
        attributes = body.get("attributes")
        package_dimensions = body.get("package_dimensions")
        metadata = body.get("metadata")
        attributes_sku = body.get("attributes_sku")
        price = body.get("price")
        inventory = body.get("inventory")
        item = stripe.Product.create(
            name=name,
            description=description,
            attributes=attributes,
            package_dimensions=package_dimensions,
            metadata=metadata
         )
        stripe.SKU.create(
            product=item.get('id'),
            attributes=attributes_sku,
            price=price,
            package_dimensions=package_dimensions,
            currency="usd",
            inventory=inventory)

        return get_object(item.id)

    @rpc
    def delete_product(self, id_product):
        """Delete a product.

        Args:
            id_product (string) The ID of the product to delete.
            sku_id (string) The ID of the SKU of product
            sku (object) object SKU to delete
            product (object) object Product to delete

        Returns:
            result (object) Returns an object with a deleted parameter on
            success.
            Otherwise, this call raises an error.

        """
        try:
            product = get_object(id_product)
            sku_id = product.skus.data[0].id
            sku = stripe.SKU.retrieve(sku_id)
            stripe.SKU.delete(sku)
            result = stripe.Product.delete(product)
        except stripe.error.InvalidRequestError as e:
            return handling(e)
        return result

    @rpc
    def update_product(self, id_product, body):
        """Updates the specific product by setting the values of the parameters
           passed.

        Note: Note that a product’s attributes are not editable.

        Args:
            id_product (string) The ID of the product to update.
            body (dict) The parameter to update.

        Returns:
            result (object) Returns the product object if the update succeeded.

        """
        try:
            product = get_object(id_product)
            for keys in body:
                product[keys] = body[keys]
            result = stripe.Product.save(product)
        except stripe.error.InvalidRequestError as e:
            return handling(e)
        return result

    @rpc
    def search_products(self, search, order_by, desc):
        """Filtering the list of products according to the specified parameter

        Args:
            search (string) parameter for search
            items (list) list of all products
            order_by (string) parameter for to ordering
            desc (bool) sorting direction
            result (list) list products sorting by search

        Returns
            result (list) sorted list products

        """
        items = stripe.Product.list(limit=100)["data"]
        if not search:
            return Products.sorted(items, order_by, desc)
        else:
            result = [it for it in items if it.get("name") == search or
                      it.metadata.get("type") == search or
                      it.metadata.get("category") == search or
                      it.metadata.get("for") == search or
                      search in it.description or
                      search == [att for att in it.attributes]]
        sort = Products.sorted(result, order_by, desc)
        return sort

    def sorted(items, sorty_value, desc):
        """Sorts the list of products according to the specified parameter

        Args:
            items (list) list of objects products
            sorty_value (str) parameter for to sorting
            desc (bool) sorting direction
            func_sort (func) function for sorting

        Returns:
            Sorted products list

        """
        def sorty_price(item):
            """Function for sort by price"""
            return item.skus.data[0].price
        if sorty_value == "price":
            func_sort = sorty_price
            return sorted(items, key=func_sort, reverse=desc)
        if not items[0].get(sorty_value):
            func_sort = operator.attrgetter('metadata.'+sorty_value)
            return sorted(items, key=func_sort, reverse=desc)
        func_sort = operator.attrgetter(sorty_value)
        return sorted(items, key=func_sort, reverse=desc)
