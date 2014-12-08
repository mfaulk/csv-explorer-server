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

    def test_dataframe_terminals(self):
        data = json.dumps({"node_type":"DataframeSource", "csv_data": base64.b64encode(self.csv_contents)})
        post_response = self.app.post('/api/v1/graph/nodes',
                           data=data,
                           content_type='application/json')
        self.assertTrue('node_id' in post_response.data)
        response_data = json.loads(post_response.data)
        node_id = response_data['node_id']

        uri = "node://" + node_id + "/B"
        get_response = self.app.get('/api/vi/graph/terminal/' + uri)
        series_data = json.loads(get_response.data)
        series_data
        # Note: the indices are strings.
        self.assertEqual(series_data['0'],11)
        self.assertEqual(series_data['1'],101)

