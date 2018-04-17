import yaml, copy, os
from .fields_parser import get_field
from collections import OrderedDict
from util.app_util import create_type_driven_func
yaml.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader, node: OrderedDict(loader.construct_pairs(node)))


def __fields_func(key, value, cursor_object):
    result = list(map(lambda item: get_field(item['field']), value))
    value.clear()
    value.extend(result)


def __replace_fields_type_driven_func_dict(_dict, func, cursor_object):
    for key, value in _dict.items():
        if key == 'fields':
            __fields_func(key, value, cursor_object)
        elif key == 'namePrefix':
            cursor_object['namePrefix'] = value
        else:
            copied_cursor_object = copy.deepcopy(cursor_object)
            if 'parent' in copied_cursor_object:
                copied_cursor_object['parent'].append(key)
            else:
                copied_cursor_object['parent'] = [key]
            func(value, copied_cursor_object)


def __replace_fields(form_yaml):
    create_type_driven_func({
        OrderedDict: __replace_fields_type_driven_func_dict
    })(form_yaml, {})
    return form_yaml


def parse_form(form_name):
    assert os.path.exists(
        'yaml/form/' + form_name + '.yml'), 'form file not found.'
    with open('yaml/form/' + form_name + '.yml') as file:
        obj = yaml.load(file)
        __replace_fields(obj)
        return obj
