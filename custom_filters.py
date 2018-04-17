from yaml_parser.form_parser import parse_form


def foo(*arg):
    return 'bar'


def get_parsed_form_yaml(form_name):
    return parse_form(form_name)


all_filters = {'get_parsed_form_yaml': get_parsed_form_yaml}


def add_all_filters(filter_object):
    for filter_name, filter in all_filters.items():
        filter_object[filter_name] = filter
