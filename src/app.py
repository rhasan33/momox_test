import json
import sys
import xml
from collections import OrderedDict

import xmltodict


def read_data_from_xml(file_path: str) -> OrderedDict:
    # takes file path as the param and returns the parsed data
    data = OrderedDict()
    try:
        with open(file=file_path) as xml_file:
            data = xmltodict.parse(xml_input=xml_file.read())
    except FileNotFoundError as err:
        print('file not found', err)
        return data
    except xml.parsers.expat.ExpatError as err:
        print('invalid xml file', err)
        return data
    return data


if __name__ == '__main__':
    data = read_data_from_xml('employee_orders.xml')
    if not data:
        sys.exit()
    # first create a json string from OrderedDict and the transforms into dictionary
    data = json.loads(json.dumps(data))
