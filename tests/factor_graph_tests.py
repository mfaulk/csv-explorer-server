import unittest
from models import *
from factors.nodes import SourceNode, FactorNode, ReportNode, DirectedEdge
from factors.factor_graph import FactorGraph
from tests.test_extensions.sample_factor import SampleFactor
import json as JSON

class TestFactorGraph(unittest.TestCase):

    def test_source_node(self):
        source_node = SourceNode()
        source_node.compute()
        #print(source_node.id)

    def test_factor_graph_initialization(self):
        fg = FactorGraph()
        self.assertEqual(len(fg.get_edges()), 0)
        self.assertEqual(len(fg.factorNodes), 0)
        self.assertEqual(len(fg.sourceNodes), 0)
        self.assertEqual(len(fg.reportNodes), 0)

    def test_factor_graph_adds(self):
        fg = FactorGraph()

        srcNode = SourceNode()
        fg.addSourceNode(srcNode)
        self.assertEqual(len(fg.sourceNodes), 1)

        factorNode = FactorNode()
        fg.addFactorNode(factorNode)
        self.assertEqual(len(fg.factorNodes), 1)

        reportNode = ReportNode()
        fg.addReportNode(reportNode)
        self.assertEqual(len(fg.reportNodes), 1)

        edge_a = DirectedEdge(srcNode, factorNode)
        edge_b = DirectedEdge(factorNode, reportNode)
        fg.addEdge(edge_a)
        self.assertEqual(len(fg.get_edges()), 1)
        fg.addEdge(edge_b)
        self.assertEqual(len(fg.get_edges()), 2)

    def test_add_factor_node_by_class_name(self):
        fg = FactorGraph()
        fg.addNode("FactorNode")
        self.assertEqual(len(fg.factorNodes.values()), 1)
        self.assertEqual(len(fg.sourceNodes.values()), 0)
        self.assertEqual(len(fg.reportNodes.values()), 0)
        self.assertTrue(isinstance(list(fg.factorNodes.values())[0], FactorNode))

    def test_add_source_node_by_class_name(self):
        fg = FactorGraph()
        fg.addNode("SourceNode")
        self.assertEqual(len(fg.factorNodes.values()), 0)
        self.assertEqual(len(fg.sourceNodes.values()), 1)
        self.assertEqual(len(fg.reportNodes.values()), 0)
        self.assertTrue(isinstance(list(fg.sourceNodes.values())[0], SourceNode))

    def test_add_report_node_by_class_name(self):
        fg = FactorGraph()
        fg.addNode("ReportNode")
        self.assertEqual(len(fg.factorNodes.values()), 0)
        self.assertEqual(len(fg.sourceNodes.values()), 0)
        self.assertEqual(len(fg.reportNodes.values()), 1)
        self.assertTrue(isinstance(list(fg.reportNodes.values())[0], ReportNode))

    def tests_add_node_by_class_name_from_extensions(self):
        fg = FactorGraph()
        fg.addNode("SampleFactor", extensions_path='tests.test_extensions')
        self.assertEqual(len(fg.factorNodes.values()), 1)
        self.assertEqual(len(fg.sourceNodes.values()), 0)
        self.assertEqual(len(fg.reportNodes.values()), 0)
        self.assertTrue(isinstance(list(fg.factorNodes.values())[0], SampleFactor))

    def test_topo_sort(self):
        src_node_a = SourceNode()
        src_node_b = SourceNode()
        factor_node_a = FactorNode()
        factor_node_b = FactorNode()
        edge_one = DirectedEdge(src_node_a, factor_node_a)
        edge_two = DirectedEdge(src_node_b, factor_node_a)
        edge_three = DirectedEdge(factor_node_a, factor_node_b)
        edge_four = DirectedEdge(src_node_a, factor_node_b)

        fg = FactorGraph()
        fg.addSourceNode(src_node_a)
        fg.addFactorNode(factor_node_a)
        fg.addSourceNode(src_node_b)
        fg.addFactorNode(factor_node_b)
        fg.addEdge(edge_one)
        fg.addEdge(edge_two)
        fg.addEdge(edge_three)
        fg.addEdge(edge_four)
        topo_sort = fg.topological_sort()
        topo_sort_ids = map(lambda node: node.id, topo_sort)
        # Assert that there are no duplicates
        self.assertEqual(len(topo_sort_ids), len(set(topo_sort_ids)))

        # Assert that the ordering respects the ordering implied by each edge
        self.assertTrue(topo_sort_ids.index(src_node_a.id) < topo_sort_ids.index(factor_node_a.id))
        self.assertTrue(topo_sort_ids.index(src_node_b.id)< topo_sort_ids.index(factor_node_a.id))
        self.assertTrue(topo_sort_ids.index(factor_node_a.id) < topo_sort_ids.index(factor_node_b.id))
        self.assertTrue(topo_sort_ids.index(src_node_a.id) < topo_sort_ids.index(factor_node_b.id))

        # The topological sort should not have changed the Factor Graph structure
        self.assertEqual(len(fg.get_edges()), 4)
        self.assertTrue(edge_one in fg.get_edges())
        self.assertTrue(edge_two in fg.get_edges())
        self.assertTrue(edge_three in fg.get_edges())
        self.assertTrue(edge_four in fg.get_edges())
        self.assertEqual(len(fg.sourceNodes), 2)
        self.assertTrue(src_node_a in fg.sourceNodes.values())
        self.assertTrue(src_node_b in fg.sourceNodes.values())
        self.assertEqual(len(fg.factorNodes), 2)
        self.assertTrue(factor_node_a in fg.factorNodes.values())
        self.assertTrue(factor_node_b in fg.factorNodes.values())

    def test_compute(self):
        src_node_a = SourceNode()
        src_node_b = SourceNode()
        factor_node_a = FactorNode()
        factor_node_b = FactorNode()
        edge_one = DirectedEdge(src_node_a, factor_node_a)
        edge_two = DirectedEdge(src_node_b, factor_node_a)
        edge_three = DirectedEdge(factor_node_a, factor_node_b)
        edge_four = DirectedEdge(src_node_a, factor_node_b)

        fg = FactorGraph()
        fg.addSourceNode(src_node_a)
        fg.addFactorNode(factor_node_a)
        fg.addSourceNode(src_node_b)
        fg.addFactorNode(factor_node_b)
        fg.addEdge(edge_one)
        fg.addEdge(edge_two)
        fg.addEdge(edge_three)
        fg.addEdge(edge_four)

    def test_graph_json(self):
        src_node_a = SourceNode()
        src_node_b = SourceNode()
        factor_node_a = FactorNode()
        factor_node_b = FactorNode()
        edge_one = DirectedEdge(src_node_a, factor_node_a)
        edge_two = DirectedEdge(src_node_b, factor_node_a)
        edge_three = DirectedEdge(factor_node_a, factor_node_b)
        edge_four = DirectedEdge(src_node_a, factor_node_b)

        fg = FactorGraph()
        fg.addSourceNode(src_node_a)
        fg.addFactorNode(factor_node_a)
        fg.addSourceNode(src_node_b)
        fg.addFactorNode(factor_node_b)
        fg.addEdge(edge_one)
        fg.addEdge(edge_two)
        fg.addEdge(edge_three)
        fg.addEdge(edge_four)

        data = JSON.loads(fg.to_json())
        self.assertTrue("nodes" in data)
        nodes = data['nodes']
        self.assertEqual(len(nodes), 4)
        self.assertTrue("edges" in data)
        edges = data['edges']
        self.assertEqual(len(edges), 4)


    def test_node_json(self):
        src_node_a = SourceNode()
        src_node_b = SourceNode()
        factor_node_a = FactorNode()
        factor_node_b = FactorNode()
        edge_one = DirectedEdge(src_node_a, factor_node_a)
        edge_two = DirectedEdge(src_node_b, factor_node_a)
        edge_three = DirectedEdge(factor_node_a, factor_node_b)
        edge_four = DirectedEdge(src_node_a, factor_node_b)

        fg = FactorGraph()
        fg.addSourceNode(src_node_a)
        fg.addFactorNode(factor_node_a)
        json = fg.nodes_to_json()
        data = JSON.loads(json)
        self.assertTrue("sources" in data)
        self.assertTrue("reports" in data)
        self.assertTrue("factors" in data)

if __name__ == '__main__':
    unittest.main()
