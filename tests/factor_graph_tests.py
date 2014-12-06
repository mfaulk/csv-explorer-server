import unittest
import pandas as pd
from factors.factor_graph import FactorGraph
from factors.context import Context
from factors.nodes import TerminalEdge as DirectedEdge

class TerminalGraphTests(unittest.TestCase):

    def setUp(self):
        self.graph = FactorGraph()
        self.df = pd.DataFrame({
            'A': 1.,
            'B': pd.Timestamp('20130102'),
            'C': pd.Series(1,index=list(range(4)),dtype='float32'),
            'D': pd.Categorical(["test","train","test","train"]),
            'E': 'foo'})

    def test_initialization(self):
        self.assertEqual(len(self.graph._nodes.values()),0)
        self.assertEqual(len(self.graph._edges.values()),0)

    def test_add_node(self):
        node_a_id = self.graph.add_node("DataframeSource", args={'df': self.df})
        self.assertEqual(len(self.graph._nodes.values()),1)
        node_b_id = self.graph.add_node("IdentityFactor", args={'input_uris': ['node://' + node_a_id + '/A']})
        self.assertEqual(len(self.graph._nodes.values()),2)

    def test_add_delete_edge(self):
        node_a_id = self.graph.add_node("DataframeSource", args={'df': self.df})
        node_b_id = self.graph.add_node("IdentityFactor", args={'input_uris': ['node://' + node_a_id + '/A']})
        src_uri = "node://" + node_a_id + '/' + 'TERMINAL'
        dest_uri = "node://" + node_b_id + '/' + 'INPUT'
        self.graph.add_edge(src_uri, dest_uri)
        self.assertEqual(len(self.graph._edges[node_a_id]), 1)
        self.assertEqual(len(self.graph._edges[node_b_id]), 1)

        edge = DirectedEdge(src_uri, dest_uri)
        self.graph.delete_edge(edge)
        self.assertEqual(len(self.graph._edges[node_a_id]), 0)
        self.assertEqual(len(self.graph._edges[node_b_id]), 0)

    def test_delete_node(self):
        node_a_id = self.graph.add_node("DataframeSource", args={'df': self.df})
        node_b_id = self.graph.add_node("IdentityFactor", args={'input_uris': ['node://' + node_a_id + '/A']})
        src_uri = "node://" + node_a_id + '/' + 'TERMINAL'
        dest_uri = "node://" + node_b_id + '/' + 'INPUT'
        self.graph.add_edge(src_uri, dest_uri)
        self.assertEqual(len(self.graph._edges[node_a_id]), 1)
        self.assertEqual(len(self.graph._edges[node_b_id]), 1)

        self.graph.delete_node(node_a_id)
        self.assertFalse(node_a_id in self.graph._nodes)
        self.assertEqual(len(self.graph._edges[node_a_id]), 0)
        self.assertEqual(len(self.graph._edges[node_b_id]), 0)

    def test_topo_sort_minimal(self):
        node_a_id = self.graph.add_node("SourceNode")
        sorted = self.graph.topological_sort(self.graph._nodes, self.graph._edges)
        self.assertEqual(len(sorted), 1)
        self.assertTrue(node_a_id in sorted)

    def test_sort(self):
        source_a_id = self.graph.add_node("DataframeSource", args={'df': self.df})
        source_b_id = self.graph.add_node("DataframeSource", args={'df': self.df})

        node_a_id = self.graph.add_node("IdentityFactor", args={'input_uris': ['node://' + source_a_id + '/A']})
        node_b_id = self.graph.add_node("IdentityFactor", args={'input_uris': ['node://' + source_a_id + '/A']})
        node_c_id = self.graph.add_node("IdentityFactor", args={'input_uris': ['node://' + source_a_id + '/A']})


        # node_a_id = self.graph.add_node("IdentityFactor")
        # node_b_id = self.graph.add_node("IdentityFactor")
        # node_c_id = self.graph.add_node("IdentityFactor")

        # Source A ---> Node A
        self.graph.add_edge("node://" + source_a_id + '/' + 'TERMINAL', "node://" + node_a_id + '/' + 'INPUT')

        # Source A ---> Node B
        self.graph.add_edge("node://" + source_a_id + '/' + 'TERMINAL', "node://" + node_b_id + '/' + 'INPUT')

        # Source B ---> Node A
        self.graph.add_edge("node://" + source_b_id + '/' + 'TERMINAL', "node://" + node_a_id + '/' + 'INPUT')

        # Node B ---> Node C
        self.graph.add_edge("node://" + node_b_id + '/' + 'OUTPUT', "node://" + node_c_id + '/' + 'INPUT')

        sorted = self.graph.topological_sort(self.graph._nodes, self.graph._edges)
        self.assertEqual(len(sorted), 5)

        # Test that the ordering respects the ordering implied by each edge
        self.assertTrue(sorted.index(source_a_id) < sorted.index(node_a_id))
        self.assertTrue(sorted.index(source_a_id) < sorted.index(node_b_id))
        self.assertTrue(sorted.index(source_b_id) < sorted.index(node_a_id))
        self.assertTrue(sorted.index(node_b_id) < sorted.index(node_c_id))


if __name__ == '__main__':
    unittest.main()
