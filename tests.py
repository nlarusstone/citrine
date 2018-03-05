import materials
import unittest
import json
from materials import database
from testdata import TestData, AddData, SearchData

class MaterialsTestCase(unittest.TestCase):

    def setUp(self):
        # I have to use separate collections instead of different 
        # databases because I'm using the free tier of MongoDB
        materials.app.config['COLLECTION'] = 'testing'
        materials.app.testing = True
        self.app = materials.app.test_client()
        with materials.app.app_context():
            self.collection = database.get_db()['testing']

    def tearDown(self):
        self.collection.drop()

    def postQuery(self, url, data):
        return self.app.post(url, data=json.dumps(data), 
                content_type='application/json')

    def queryAdd(self, data):
        return self.postQuery('/data/add', data)

    def querySearch(self, data):
        return self.postQuery('/data/search', data)

    def test_empty(self):
        res = self.queryAdd(TestData.empty)
        self.assertEqual(res.status_code, 400)

        res2 = self.querySearch(TestData.empty)
        self.assertEqual(res2.status_code, 400)

    # Test add endpoint
    def test_add_compound_no_props(self):
        self.queryAdd(AddData.compoundNoProps)
        compound = self.collection.find({'compound': 
            {'$eq': AddData.compoundNoProps['compound']}})
        self.assertTrue(compound.count() > 0)

    def test_add_compound_prop(self):
        self.queryAdd(AddData.compoundProp)
        compound = self.collection.find_one({'compound': 
            {'$eq': AddData.compoundProp['compound']}})
        self.assertIn('properties', compound)

    def test_add_compound_props(self):
        self.queryAdd(AddData.compoundProps)
        compound = self.collection.find_one({'compound': 
            {'$eq': AddData.compoundProps['compound']}})
        self.assertIn('properties', compound)
        self.assertTrue(len(compound['properties']) > 0)

    def test_add_compound_extra_props(self):
        res = self.queryAdd(AddData.compoundExtraProps)
        self.assertEqual(res.status_code, 400)

    def test_add_no_compound(self):
        res = self.queryAdd(AddData.noCompound)
        self.assertEqual(res.status_code, 400)

    # Test search endpoint
    def test_search_compound_no_props(self):
        self.queryAdd(AddData.compoundNoProps)
        res = self.querySearch(SearchData.compoundNoProps)
        res_data = json.loads(res.data)
        self.assertNotEqual(res_data, [])
        pass

    def test_search_compound_prop(self):
        self.queryAdd(AddData.compoundProp)
        self.queryAdd(AddData.compoundExtraProps)
        res = self.querySearch(SearchData.compoundProp)
        res_data = json.loads(res.data)
        self.assertEqual(len(res_data), 1)
        pass

    def test_search_no_compound(self):
        self.queryAdd(AddData.compoundProp)
        self.queryAdd(AddData.compoundProps)
        res = self.querySearch(SearchData.noCompound)
        res_data = json.loads(res.data)
        self.assertEqual(len(res_data), 1)
        pass

    def test_search_wrong_compound(self):
        self.queryAdd(AddData.compoundExtraProps)
        res = self.querySearch(SearchData.compoundProp)
        res_data = json.loads(res.data)
        self.assertEqual(res_data, [])
        pass

    def test_search_multiple_results(self):
        self.queryAdd(AddData.compoundProp)
        self.queryAdd(AddData.compoundProps)
        self.queryAdd(AddData.compoundExtraProps)
        res = self.querySearch(SearchData.compoundProp)
        res_data = json.loads(res.data)
        self.assertEqual(len(res_data), 2)
        pass

if __name__ == '__main__':
    unittest.main()
