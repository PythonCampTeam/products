import cerberus

schema = {'name': {'type': 'string'},
'attributes': {'type': 'list'},
'description': {'type': 'string'},
'package_dimensions':
{'type': 'dict',
'schema':
{'height': {'type': 'float'},
'width': {'type': 'float'},
'weight': {'type': 'float'},
'length': {'type': 'float'}
}, 'metadata':
{'type': 'dict',
'schema':
'category': {'type': 'string'},
'for':  {'type': 'string'},
'type': {'type': 'string'} },
'attributes_sku' : {'type': 'dict'},
'price':  {'type': 'integer'},
'inventory': {'type': 'dict',
'schema':
{'type':{'type': 'string'},
'quantity': {'type': 'integer'}
}
}
}
}
