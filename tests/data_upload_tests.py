import unittest
import json
import base64
import pandas as pd
from factors.factor_graph import FactorGraph
import app

class DataUploadtests(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        # Re-initialize the factor graph between tests.
        app.factor_graph = FactorGraph()
        self.csv_contents = '''A,B,C
    10,11,12
    100,101,102'''

    def test_dataframe_source_csv_upload(self):
        data = json.dumps({"node_type":"DataframeSource", "csv_data": base64.b64encode(self.csv_contents)})
        post_response = self.app.post('/api/v1/graph/nodes',
                           data=data,
                           content_type='application/json')
        self.assertTrue('node_id' in post_response.data)
        response_data = json.loads(post_response.data)
        node_id = response_data['node_id']

        # Retrieve tabular data
        get_response = self.app.get('/api/v1/graph/node/' + node_id)
        data_dict = json.loads(get_response.data)
        data_dict
        dataframe_contents = data_dict['df']
        dataframe_contents
        contents = dict()
        for key, value in dataframe_contents.iteritems():
            contents[key] = pd.Series(value)
        self.assertEqual(set(['A','B','C']), set(contents.keys()))

        seriesA = contents['A']
        self.assertEqual(seriesA[0],10)
        self.assertEqual(seriesA[1],100)

        seriesB = contents['B']
        self.assertEqual(seriesB[0],11)
        self.assertEqual(seriesB[1],101)

        seriesC = contents['C']
        self.assertEqual(seriesC[0],12)
        self.assertEqual(seriesC[1],102)


