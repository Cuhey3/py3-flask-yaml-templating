import copy
from collections import OrderedDict


def create_type_driven_func(arg={}, returning=False):
    def func(any_type_data, cursor_object):
        _type = type(any_type_data)
        if _type in arg:
            if returning:
                any_type_data = arg[_type](any_type_data, func, cursor_object)
            else:
                arg[_type](any_type_data, func, cursor_object)
        return any_type_data

    return func


def __get_nested_value_dict(_dict_data, func, cursor_object):
    path_list = cursor_object['path']
    if len(path_list) == 0:
        return _dict_data
    else:
        path_key = path_list.pop(0)
        if path_key in _dict_data:
            if len(path_list) == 0:
                return _dict_data[path_key]
            else:
                return func(_dict_data[path_key], func, cursor_object)
        else:
            return cursor_object['default_value']


__get_nested_value_driven_func = create_type_driven_func(
    {
        dict: __get_nested_value_dict,
        OrderedDict: __get_nested_value_dict
    }, True)


def get_nested_value(any_type_data, path_list, default_value=None):
    if type(path_list) == str:
        path_list = path_list.split('.')
    assert type(path_list) == list, 'path argument must be a string or a list'
    return __get_nested_value_driven_func(any_type_data, {
        'path': path_list,
        'default_value': default_value
    })
