def foo(*arg):
    return 'bar'


all_filters = {'foo': foo}


def add_all_filters(filter_object):
    for filter_name, filter in all_filters.items():
        filter_object[filter_name] = filter
