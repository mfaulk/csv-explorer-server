import unittest
from models import *
from factors.nodes import SourceNode, FactorNode, ReportNode, DirectedEdge
from factors.factor_graph import FactorGraph

class TestFactorGraph(unittest.TestCase):

    def test_source_node(self):
        table = "table"
        source_node = SourceNode(table)
        source_node.compute()
        print(source_node.id)

    def test_factor_graph_initialization(self):
        fg = FactorGraph()
        self.assertEqual(len(fg.get_edges()), 0)
        self.assertEqual(len(fg.factorNodes), 0)
        self.assertEqual(len(fg.sourceNodes), 0)
        self.assertEqual(len(fg.reportNodes), 0)

    def test_factor_graph_adds(self):
        fg = FactorGraph()

        srcNode = SourceNode('table')
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

    def test_topo_sort(self):
        src_node_a = SourceNode(table="table", name="Source A")
        src_node_b = SourceNode(table="table", name="Source B")
        factor_node_a = FactorNode("Factor A")
        factor_node_b = FactorNode("Factor B")
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
        topo_sort_names = map(lambda node: node.name, topo_sort)
        # Assert that there are no duplicates
        self.assertEqual(len(topo_sort_names), len(set(topo_sort_names)))

        # Assert that the ordering respects the ordering implied by each edge
        self.assertTrue(topo_sort_names.index("Source A") < topo_sort_names.index("Factor A"))
        self.assertTrue(topo_sort_names.index("Source B") < topo_sort_names.index("Factor A"))
        self.assertTrue(topo_sort_names.index("Factor A") < topo_sort_names.index("Factor B"))
        self.assertTrue(topo_sort_names.index("Source A") < topo_sort_names.index("Factor B"))

        # The topological sort should not have changed the Factor Graph structure
        self.assertEqual(len(fg.get_edges()), 4)
        self.assertTrue(edge_one in fg.get_edges())
        self.assertTrue(edge_two in fg.get_edges())
        self.assertTrue(edge_three in fg.get_edges())
        self.assertTrue(edge_four in fg.get_edges())
        self.assertEqual(len(fg.sourceNodes), 2)
        self.assertTrue(src_node_a in fg.sourceNodes)
        self.assertTrue(src_node_b in fg.sourceNodes)
        self.assertEqual(len(fg.factorNodes), 2)
        self.assertTrue(factor_node_a in fg.factorNodes)
        self.assertTrue(factor_node_b in fg.factorNodes)

    def test_compute(self):
        src_node_a = SourceNode(table="table", name="Source A")
        src_node_b = SourceNode(table="table", name="Source B")
        factor_node_a = FactorNode("Factor A")
        factor_node_b = FactorNode("Factor B")
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
        src_node_a = SourceNode(table="table", name="Source A")
        src_node_b = SourceNode(table="table", name="Source B")
        factor_node_a = FactorNode("Factor A")
        factor_node_b = FactorNode("Factor B")
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

        print(fg.to_json())

    def test_node_json(self):
        src_node_a = SourceNode(table="table", name="Source A")
        src_node_b = SourceNode(table="table", name="Source B")
        factor_node_a = FactorNode("Factor A")
        factor_node_b = FactorNode("Factor B")
        edge_one = DirectedEdge(src_node_a, factor_node_a)
        edge_two = DirectedEdge(src_node_b, factor_node_a)
        edge_three = DirectedEdge(factor_node_a, factor_node_b)
        edge_four = DirectedEdge(src_node_a, factor_node_b)

        fg = FactorGraph()
        fg.addSourceNode(src_node_a)
        fg.addFactorNode(factor_node_a)
        json = fg.nodes_to_json()
        print(json)

if __name__ == '__main__':
    unittest.main()
