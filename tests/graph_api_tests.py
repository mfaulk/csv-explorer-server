import unittest
import json
from factors.factor_graph import FactorGraph
import app

class GraphApiTests(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        # Re-initialize the factor graph between tests
        app.factor_graph = FactorGraph()

    def test_empty_graph(self):
        rv = self.app.get('/api/v1/graph')
        expected = {
            "nodes": [],
            "edges": []
        }
        self.assertEqual(json.loads(rv.data), expected)

    def test_factors(self):
        rv = self.app.get('/api/v1/factors')
        self.assertEqual(rv.status, "200 OK")

        expected = {"factor-types": [
            {"class_name": "IdentityFactor",
             "out": [{"type": "STRING", "name": "OUTPUT"}],
             "in": [{"type": "STRING", "name": "INPUT"}]}]
        }

        self.assertEqual(json.loads(rv.data), expected)

    def test_empty_nodes(self):
        rv = self.app.get('/api/v1/graph/nodes')
        expected = {
            "nodes": []
        }
        self.assertEqual(json.loads(rv.data), expected)

    def test_post_node(self):
        data = json.dumps({"node_type":"IdentityFactor"})
        rv = self.app.post('/api/v1/graph/nodes',
                           data=data,
                           content_type='application/json')
        self.assertTrue('node_id' in rv.data)

        nodes_response = self.app.get('/api/v1/graph/nodes')
        self.assertTrue('nodes' in nodes_response.data)
        nodes = json.loads(nodes_response.data)['nodes']
        self.assertEqual(len(nodes), 1)

    def test_delete_node(self):
        data = json.dumps({"node_type":"IdentityFactor"})
        rv = self.app.post('/api/v1/graph/nodes',
                           data=data,
                           content_type='application/json')
        node_id = json.loads(rv.data)['node_id']

        delete_response = self.app.delete('/api/v1/graph/node/' + node_id)
        self.assertTrue('node_id' in json.loads(delete_response.data))

        nodes_response = self.app.get('/api/v1/graph/nodes')
        self.assertTrue('nodes' in nodes_response.data)
        nodes = json.loads(nodes_response.data)['nodes']
        self.assertEqual(len(nodes), 0)


    def test_post_two_nodes(self):
        data = json.dumps({"node_type":"IdentityFactor"})
        self.app.post('/api/v1/graph/nodes',
                           data=data,
                           content_type='application/json')

        self.app.post('/api/v1/graph/nodes',
                           data=data,
                           content_type='application/json')

        nodes_response = self.app.get('/api/v1/graph/nodes')
        self.assertTrue('nodes' in nodes_response.data)
        nodes = json.loads(nodes_response.data)['nodes']
        self.assertEqual(len(nodes), 2)

    def _num_edges(self, rv):
        return len(json.loads(rv.data)['edges'])


    def test_add_delete_edges(self):
        node_a_response = self.app.post('/api/v1/graph/nodes',
                           data=json.dumps({"node_type":"IdentityFactor"}),
                           content_type='application/json')
        node_a_id = json.loads(node_a_response.data)['node_id']

        node_b_response = self.app.post('/api/v1/graph/nodes',
                           data=json.dumps({"node_type":"IdentityFactor"}),
                           content_type='application/json')
        node_b_id = json.loads(node_b_response.data)['node_id']


        edge_data = {"src_uri": "node://" + node_a_id + "/OUTPUT",
                    "dest_uri": "node://" + node_b_id + "/INPUT"}

        rv = self.app.post('/api/vi/graph/edges',
                      data=json.dumps(edge_data),
                      content_type='application/json')
        self.assertTrue("edge_id" in json.loads(rv.data))

        response = self.app.get('/api/vi/graph/edges')
        edges = json.loads(response.data)
        self.assertTrue("edges" in edges)
        self.assertEqual(len(edges["edges"]),1)

        # Add another edge
        edge_two_data = {"src_uri": "node://" + node_a_id + "/FOO",
                    "dest_uri": "node://" + node_b_id + "/Bar"}

        rv = self.app.post('/api/vi/graph/edges',
                      data=json.dumps(edge_two_data),
                      content_type='application/json')

        response_two = self.app.get('/api/vi/graph/edges')
        response_two_data = json.loads(response_two.data)
        self.assertTrue("edges" in response_two_data)
        self.assertEqual(len(response_two_data["edges"]),2)

        edge_list = response_two_data['edges']
        edge_id_one = edge_list[0]['id']
        edge_id_two = edge_list[1]['id']

        self.app.delete('/api/vi/graph/edges/' + edge_id_one)
        self.assertEqual(self._num_edges(self.app.get('/api/vi/graph/edges')), 1)

        self.app.delete('/api/vi/graph/edges/' + edge_id_two)
        self.assertEqual(self._num_edges(self.app.get('/api/vi/graph/edges')), 0)

