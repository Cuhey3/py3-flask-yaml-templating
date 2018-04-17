import yaml, copy
from .fields_parser import get_field
from collections import OrderedDict
from util.app_util import create_type_driven_func
yaml.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader, node: OrderedDict(loader.construct_pairs(node)))


def fields_func(key, value, cursor_object):
    for item in value:
        item['field'] = get_field(item['field'])


def replace_fields_type_driven_func_dict(_dict, func, cursor_object):
    for key, value in _dict.items():
        if key == 'fields':
            fields_func(key, value, cursor_object)
        elif key == 'namePrefix':
            cursor_object['namePrefix'] = value
        else:
            copied_cursor_object = copy.deepcopy(cursor_object)
            if 'parent' in copied_cursor_object:
                copied_cursor_object['parent'].append(key)
            else:
                copied_cursor_object['parent'] = [key]
            func(value, copied_cursor_object)


def replace_fields(form_yaml):
    create_type_driven_func({
        OrderedDict: replace_fields_type_driven_func_dict
    })(form_yaml, {})
    return form_yaml


def parse_form(form_name):
    with open('yaml/form/' + form_name + '.yml') as file:
        obj = yaml.load(file)
        replace_fields(obj)
        return obj
