import unittest
from factors.factor_graph import FactorGraph
from factors.nodes import TerminalEdge as DirectedEdge

class TerminalGraphTests(unittest.TestCase):

    def setUp(self):
        self.graph = FactorGraph()

    def test_initialization(self):
        self.assertEqual(len(self.graph._nodes.values()),0)
        self.assertEqual(len(self.graph._edges.values()),0)

    def test_add_node(self):
        self.graph.addNode("IdentityFactor")
        self.assertEqual(len(self.graph._nodes.values()),1)
        self.graph.addNode("SourceNode")
        self.assertEqual(len(self.graph._nodes.values()),2)

    def test_add_delete_edge(self):
        node_a_id = self.graph.addNode("SourceNode")
        node_b_id = self.graph.addNode("IdentityFactor")
        src_uri = "node://" + node_a_id + '/' + 'TERMINAL'
        dest_uri = "node://" + node_b_id + '/' + 'INPUT'
        self.graph.addEdge(src_uri, dest_uri)
        self.assertEqual(len(self.graph._edges[node_a_id]), 1)
        self.assertEqual(len(self.graph._edges[node_b_id]), 1)

        edge = DirectedEdge(src_uri, dest_uri)
        self.graph.deleteEdge(edge)
        self.assertEqual(len(self.graph._edges[node_a_id]), 0)
        self.assertEqual(len(self.graph._edges[node_b_id]), 0)

    def test_delete_node(self):
        node_a_id = self.graph.addNode("SourceNode")
        node_b_id = self.graph.addNode("IdentityFactor")
        src_uri = "node://" + node_a_id + '/' + 'TERMINAL'
        dest_uri = "node://" + node_b_id + '/' + 'INPUT'
        self.graph.addEdge(src_uri, dest_uri)
        self.assertEqual(len(self.graph._edges[node_a_id]), 1)
        self.assertEqual(len(self.graph._edges[node_b_id]), 1)

        self.graph.deleteNode(node_a_id)
        self.assertFalse(node_a_id in self.graph._nodes)
        self.assertEqual(len(self.graph._edges[node_a_id]), 0)
        self.assertEqual(len(self.graph._edges[node_b_id]), 0)

    def test_topo_sort_minimal(self):
        node_a_id = self.graph.addNode("SourceNode")
        sorted = self.graph.topological_sort(self.graph._nodes, self.graph._edges)
        self.assertEqual(len(sorted), 1)
        self.assertTrue(node_a_id in sorted)

    def test_sort_small(self):
        source_a_id = self.graph.addNode("SourceNode")
        node_b_id = self.graph.addNode("IdentityFactor")
        node_c_id = self.graph.addNode("IdentityFactor")

        self.graph.addEdge("node://" + source_a_id + '/' + 'TERMINAL', "node://" + node_b_id + '/' + 'INPUT')
        self.graph.addEdge("node://" + node_b_id + '/' + 'OUTPUT', "node://" + node_c_id + '/' + 'INPUT')

        sorted = self.graph.topological_sort(self.graph._nodes, self.graph._edges)
        self.assertEqual(len(sorted), 3)
        self.assertEqual(source_a_id, sorted[0])
        self.assertEqual(node_b_id, sorted[1])
        self.assertEqual(node_c_id, sorted[2])

    def test_sort_medium(self):
        source_a_id = self.graph.addNode("SourceNode")
        source_b_id = self.graph.addNode("SourceNode")

        node_a_id = self.graph.addNode("IdentityFactor")
        node_b_id = self.graph.addNode("IdentityFactor")
        node_c_id = self.graph.addNode("IdentityFactor")

        # Source A ---> Node A
        self.graph.addEdge("node://" + source_a_id + '/' + 'TERMINAL', "node://" + node_a_id + '/' + 'INPUT')

        # Source A ---> Node B
        self.graph.addEdge("node://" + source_a_id + '/' + 'TERMINAL', "node://" + node_b_id + '/' + 'INPUT')

        # Source B ---> Node A
        self.graph.addEdge("node://" + source_b_id + '/' + 'TERMINAL', "node://" + node_a_id + '/' + 'INPUT')

        # Node B ---> Node C
        self.graph.addEdge("node://" + node_b_id + '/' + 'OUTPUT', "node://" + node_c_id + '/' + 'INPUT')

        sorted = self.graph.topological_sort(self.graph._nodes, self.graph._edges)
        self.assertEqual(len(sorted), 5)

        # Test that the ordering respects the ordering implied by each edge
        self.assertTrue(sorted.index(source_a_id) < sorted.index(node_a_id))
        self.assertTrue(sorted.index(source_a_id) < sorted.index(node_b_id))
        self.assertTrue(sorted.index(source_b_id) < sorted.index(node_a_id))
        self.assertTrue(sorted.index(node_b_id) < sorted.index(node_c_id))


if __name__ == '__main__':
    unittest.main()
