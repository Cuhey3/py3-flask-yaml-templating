import yaml, os
from collections import OrderedDict
yaml.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader, node: OrderedDict(loader.construct_pairs(node)))


def fields_enrich(fields):
    for key, value in fields.items():
        if value is None:
            value = {}
        if not 'label' in value:
            value['label'] = key
        fields[key] = value


fields_yaml_file_names = []
fields_namespaces = {}
for root, dirs, files in os.walk("yaml/fields"):
    for filename in files:
        if filename.endswith('.yml'):
            fields_yaml_file_names.append(os.path.join(root, filename))
    for dirname in dirs:
        fields_yaml_file_names.append(os.path.join(root, dirname))

for fields_yaml_file_name in fields_yaml_file_names:
    with open(fields_yaml_file_name) as file:
        fields_yaml = yaml.load(file)
        namespace = fields_yaml['namespace']
        fields_namespaces[namespace] = fields_yaml['fields']
        fields_enrich(fields_namespaces[namespace])


def get_field(token):
    namespace = token.split('.')[0]
    field = token.split('.')[1]
    return fields_namespaces[namespace][field]
