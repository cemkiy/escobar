import json


def percentage(part, whole):
    return 100 * float(part) / float(whole)


def write_file(file_name, data):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)


def read_file(file_name):
    data = {}
    with open(file_name) as data_file:
        data = json.load(data_file)
    return data
