class TestData(object):
    empty = {}

class AddData(TestData):
    compoundNoProps = {'compound': 'GaN1'}
    compoundProp = {'compound': 'GaN2', 'properties': 
                     [
                       {'propertyName': 'Band gap', 'propertyValue': '3.4'}
                     ]
                   }
    compoundProps = {'compound': 'GaN3', 'properties': 
                      [
                        {'propertyName': 'Band gap', 'propertyValue': '3.6'},
                        {'propertyName': 'Color', 'propertyValue': 'Blue'}
                      ]
                    }
    compoundExtraProps = {'compound': 'GaN4', 'properties': 
                           [
                             {'propertyName': 'Band gap', 'propertyValue': '3.8'}
                           ],
                           'nonsense': 'not_inserted'
                         }
    noCompound = {'properties': 
                   [
                     {'propertyName': 'Band gap', 'propertyValue': '4.0'}
                   ]
                 }

class SearchData(TestData):
    compoundNoProps = {'compound': {'logic': 'contains', 'value': 'GaN1'}}
    compoundProp = {'compound': {'logic': 'contains', 'value': 'GaN2'}, 'properties':
                     [
                       {'name': 'Band gap', 'value': '3.6', 'logic': 'eq'}
                     ]
                   }
    compoundProps = {'compound': {'logic': 'contains', 'value': 'GaN2'}, 'properties':
                     [
                       {'name': 'Band gap', 'value': '3.6', 'logic': 'eq'},
                       {'name': 'Color', 'value': 'Blue', 'logic': 'eq'}
                     ]
                   }
    noCompound = {'properties': 
                   [
                     {'name': 'Band gap', 'value': '3.4', 'logic': 'gt'}
                   ]
                 }
