import unittest
import factors.node_factory
from factors.nodes import SourceNode, FactorNode
from tests.test_extensions.sample_factor import SampleFactor
from factors.context import Context

class NodeFactoryTest(unittest.TestCase):
    def setUp(self):
        self.context = Context()

    def test_instantiate_source_node(self):
        obj = factors.node_factory.get_instance("SourceNode", self.context)
        self.assertTrue(isinstance(obj, SourceNode))

    def test_instantiate_factor_node(self):
        obj = factors.node_factory.get_instance("FactorNode", self.context)
        self.assertTrue(isinstance(obj, FactorNode))

    def test_instance_from_extensions(self):
        obj = factors.node_factory.get_instance_from_extensions("SampleFactor", self.context, extensions_path="tests.test_extensions")
        self.assertEqual(obj.__class__, SampleFactor)

    def test_instance(self):
        obj = factors.node_factory.get_instance("SampleFactor", self.context, extensions_path="tests.test_extensions")
        self.assertEqual(obj.__class__, SampleFactor)

if __name__ == '__main__':
    unittest.main()
