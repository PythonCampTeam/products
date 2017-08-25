schema_product = {'name': {'type': 'string', 'empty': False, 'required': True},
                  'attributes': {'type': 'list'},
                  'description': {'type': 'string'},
                  'package_dimensions':
                  {'type': 'dict',  'empty': False, 'required': True,
                                    'schema':
                                    {'height':
                                     {'type': 'float',
                                      'empty': False,
                                      'required': True},
                                     'width':
                                     {'type': 'float',
                                      'empty': False,
                                      'required': True},
                                     'weight':
                                     {'type': 'float',
                                      'empty': False,
                                      'required': True},
                                     'length':
                                     {'type': 'float',
                                      'empty': False,
                                      'required': True}
                                     }},
                  'metadata': {'type': 'dict', 'empty': False,
                               'required': True, 'schema':
                                               {'category':
                                                {'type': 'string',
                                                 'empty': False,
                                                 'required': True},
                                                'for':
                                                {'type': 'string',
                                                 'empty': False,
                                                 'required': True},
                                                'type': {'type': 'string'}
                                                }},
                  'attributes_sku': {'type': 'dict',
                                     'dependencies': 'attributes'},
                  'price':  {'type': 'integer', 'empty': False,
                             'required': True},
                  'inventory': {'type': 'dict', 'empty': False,
                                'required': True, 'schema':
                                                {'type':
                                                 {'type': 'string',
                                                  'empty': False,
                                                  'required': True},
                                                 'quantity':
                                                 {'type': 'integer',
                                                  'empty': False,
                                                  'required': True}
                                                 }
                                }
                  }
