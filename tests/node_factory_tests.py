import unittest
import factors.node_factory
from factors.nodes import SourceNode, FactorNode, ReportNode
from tests.test_extensions.sample_factor import SampleFactor

class NodeFactoryTest(unittest.TestCase):

    def test_instantiate_source_node(self):
        obj = factors.node_factory.get_instance("SourceNode")
        self.assertTrue(isinstance(obj, SourceNode))

    def test_instantiate_factor_node(self):
        obj = factors.node_factory.get_instance("FactorNode")
        self.assertTrue(isinstance(obj, FactorNode))

    def test_instantiate_report_node(self):
        obj = factors.node_factory.get_instance("ReportNode")
        self.assertTrue(isinstance(obj, ReportNode))

    def test_instance_from_extensions(self):
        obj = factors.node_factory.get_instance_from_extensions("SampleFactor", extensions_path="tests.test_extensions")
        self.assertEqual(obj.__class__, SampleFactor)

    def test_instance(self):
        obj = factors.node_factory.get_instance("SampleFactor", extensions_path="tests.test_extensions")
        self.assertEqual(obj.__class__, SampleFactor)

if __name__ == '__main__':
    unittest.main()
