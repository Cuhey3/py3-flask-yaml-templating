import yaml


def parse_form(form_name):
    with open('yaml/form/' + form_name + '.yml') as file:
        obj = yaml.load(file)
        return obj
