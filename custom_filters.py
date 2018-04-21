from yaml_parser.form_parser import parse_form
from util.app_util import get_nested_value


def foo(*arg):
    return 'bar'


def get_yaml_data(data_path):
    assert data_path and type(data_path) == str, 'data path required as str'
    split_path = data_path.split('.')
    form_data = parse_form(split_path.pop(0))
    return get_nested_value(form_data, split_path)


def get_parsed_form_yaml(form_name):
    return parse_form(form_name)


all_filters = {
    'get_parsed_form_yaml': get_parsed_form_yaml,
    'get_yaml_data': get_yaml_data
}


def add_all_filters(filter_object):
    for filter_name, filter in all_filters.items():
        filter_object[filter_name] = filter
