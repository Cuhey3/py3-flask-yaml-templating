import yaml, os
from collections import OrderedDict
yaml.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader, node: OrderedDict(loader.construct_pairs(node)))

__file_names = []
__fields_namespaces = {}


def __enrich_fields(fields):
    for key, value in fields.items():
        assert value is None or type(
            value) == OrderedDict, 'value of enrich field must be dict: ' + key
        if value is None:
            value = {}
        if not 'label' in value:
            value['label'] = key
        fields[key] = value


for root, dirs, files in os.walk("yaml/fields"):
    for file_name in files:
        if file_name.endswith('.yml'):
            __file_names.append(os.path.join(root, file_name))
        else:
            print('ignore file: ', os.path.join(root, file_name),
                  'on fields_parser')

for file_name in __file_names:
    with open(file_name) as file:
        yaml_data = yaml.load(file)
        assert yaml_data, 'fields yaml is empty: ' + file_name
        assert 'namespace' in yaml_data and yaml_data['namespace'], 'fields yaml requires namespace: ' + file_name
        namespace = yaml_data['namespace']
        assert type(
            namespace
        ) == str, 'fields yaml namespace needs to be a str: ' + file_name
        assert 'fields' in yaml_data and yaml_data['fields'], 'fields yaml does not have fields: ' + file_name
        fields = yaml_data['fields']
        assert type(
            fields) == OrderedDict, 'fields value must be dict: ' + file_name
        __fields_namespaces[namespace] = fields
        __enrich_fields(__fields_namespaces[namespace])


def get_field(token):
    assert '.' in token, 'no namespace found in field specification: ' + token
    namespace = token.split('.')[0]
    assert namespace in __fields_namespaces, 'non-existent namespace: ' + namespace
    fields = __fields_namespaces[namespace]
    assert fields, 'namespace exists, but it has no value: ' + namespace
    field_name = token.split('.')[1]
    assert field_name in fields, 'field name does not exist: ' + token
    field = fields[field_name]
    assert field, 'field name exists but has no value.'
    return field
