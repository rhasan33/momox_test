import json
import sys
import xml
from collections import OrderedDict
from typing import Dict, List

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


def get_full_menu() -> Dict:
    # this function will make dummy request to get the menu
    menu = dict()
    # here need to handle the request
    try:
        '''
        need to check the api call. requests library can be used here
        like: requests.get('https://nourish.me/api/v1/menu)
        first need to check the api status code after making the request
        if the status code is 200 (in a ideal situation) then we can proceed
        else return an empty dict
        '''
        with open('menu.json') as f:
            menu = json.load(f)
    except json.decoder.JSONDecodeError:
        # handle requests exceptions like ReadTimeout, ConnectionError, ConnectionTimeout
        print('cannot read json file')
        sys.exit()
    return menu


def get_item_id_from_menu(item_name: str) -> int:
    # the function takes item_name as the parameter and returns the assiciated item_id
    menu = get_full_menu()
    # to maintain the return type 0 is returned
    if not menu:
        print('no menu found')
        sys.exit()
    # check from the menu by name and trying to get the id
    for data in menu['dishes']:
        if item_name.strip() == data['name']:
            return data['id']
    return 0


def item_id_with_amount(item_data: str) -> List[Dict]:
    '''
    this function takes item data chosen by the employee for the meal and retuens the
    list of dictionary with item id and amount (quantity of food item)
    '''
    item_list = []
    # first split the string by comma to get all the food items name and amount
    items = item_data.split(',')
    for item in items:
        # again spliting the text by `x` that and separate the item info from string
        item_info = item.split('x')
        # pass the name of the item from the list index[1] to get_item_id_from_menu function and get the item id
        item_list.append({
            'id': get_item_id_from_menu(item_info[1]),
            'amount': int(item_info[0]),
        })
    return item_list


def create_order_request_body(data: Dict) -> Dict:
    # the function takes emplyee data in dictionary and retuns the create order request body
    employees_data = dict()
    employees_data['orders'] = []
    for employee in data['Employees']['Employee']:
        # eleminating those who are not attending the program
        if employee['IsAttending'] != 'true':
            continue
        emp = {
            'customer': {
                'full_name': employee['Name'],
                'address': {
                    'street': employee['Address']['Street'],
                    'city': employee['Address']['City'],
                    'postal_code': employee['Address']['PostalCode'],
                }
            },
            'items': item_id_with_amount(employee['Order']),
        }
        employees_data['orders'].append(emp)
    return employees_data


def place_order(body: Dict) -> str:
    try:
        '''
        make a post request with the body to nourish.me
        example: requests.post('https://nourish.me/api/v1/bulk/order', json=body)
        no need to pass content type as body is passed as json
        '''
    except Exception as err:
        '''
        handle requests exceptions
        returns order not created
        '''
    return 'order created'


if __name__ == '__main__':
    data = read_data_from_xml('employee_orders.xml')
    if not data:
        sys.exit()
    # first create a json string from OrderedDict and the transforms into dictionary
    data = json.loads(json.dumps(data))
    create_order = create_order_request_body(data)
    with open('orders.json', 'w') as json_file:
        json.dump(create_order, json_file, indent=4)
    order = place_order(create_order)
    print(order)
