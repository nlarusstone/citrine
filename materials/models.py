import re
from materials import app
from .database import db
from . import errors
from .constants import valid_logic, numerical_logic
from pymongo.errors import WriteError

""" 
    data - JSON data from the request
    returns a tuple of a message and the status code
"""
def add_to_db(data):
    collection = db[app.config['COLLECTION']]
    if 'compound' not in data:
        return ('Need to specify a compound to add', 400)
    # Should only specify a compound and propreties
    if len(data.keys()) > 2:
        return ('Too many fields', 400)
    for k in data.keys():
        if not k in ['compound', 'properties']:
            return ('The only fields allowed are compound and properties', 400)
    # Only looks for exact matches based on name
    compound = collection.find({'compound': {'$eq': data['compound']}})
    if compound.count() > 0:
        return ('Compound already in database, please use PATCH to update', 409)
    try:
        res = collection.insert_one(data)
    except WriteError:
        return ('Compound failed to add', 503)
    if 'properties' not in data:
        response = 'Compound added without any properties'
    else:
        response = 'Compound successfully added'
    return (response, 200)

""" 
    data - JSON data from the request
    Note: will return entries that satsify any of the requirements 
    (Acts as an OR on the compound and all the properties)
    returns a tuple of a message and the status code
"""
def search_db(data):
    collection = db[app.config['COLLECTION']]
    query = []
    # Find by compound name
    if 'compound' in data:
        compound_query_fields = data['compound']
        if compound_query_fields:
            compound_logic = compound_query_fields['logic'].lower()
            if not valid_logic_field(compound_logic):
                return ("Compound's logic field is invalid", 400)
            if compound_logic == 'contains':
                query_body = {'$regex': '.*{0}.*'.format(compound_query_fields['value'])}
            else:
                query_body = {'$' + compound_logic: compound_query_fields['value']}
            query.append({'compound': query_body})

    # Find by properties
    if 'properties' in data:
        for prop in data['properties']:
            # Logic is case insensitive and always worked with in lower case
            logic = prop['logic'].lower()
            if not valid_logic_field(logic):
                return ('Property {0} has an invalid logic field'.format(prop['name']), 400)
            if prop['logic'] in numerical_logic:
                try:
                    float(prop['value'])
                except ValueError:
                    return ('{0} is numerical logic, but {1} is not a number'.format(
                         logic, prop['value']), 400)
                query_body = {'${0}'.format(logic): prop['value']}
            else:
                # Property values and names are both case sensitive
                query_body = {'${0}'.format(logic): prop['value']}
            query.append({'properties' : {'$elemMatch': 
                                    {'propertyName': prop['name'],
                                    'propertyValue': query_body}}})

    if not query:
        return ("No compound or properties specified", 400)
    results = collection.find({'$or': query}, {'_id': False})
    return (results, 200)

"""
    logic - "logic" field from the request JSON object
    returns True if the field is a recognized logic abbreviation
"""
def valid_logic_field(logic):
    if not logic in valid_logic:
        return False
    else:
        return True
