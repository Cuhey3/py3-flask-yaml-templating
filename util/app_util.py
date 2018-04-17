import copy


def create_type_driven_func(arg={}):
    def func(any_type_data, cursor_object):
        _type = type(any_type_data)
        if _type in arg:
            arg[_type](any_type_data, func, cursor_object)
        return any_type_data

    return func
