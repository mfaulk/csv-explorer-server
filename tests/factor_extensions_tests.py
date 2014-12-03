import unittest
from framework import package_contents, subclasses_in_module, subclasses_in_package, get_factor_extensions
from test_extensions import sample_factor
from factors.nodes import FactorNode

class TestModels(unittest.TestCase):

    def test_extensions(self):
        modules, pathname = package_contents('test_extensions')
        self.assertTrue('__init__' in modules)
        self.assertTrue('sample_factor' in modules)

    def test_factor_subclasses(self):
        klasses = subclasses_in_module(FactorNode, sample_factor)
        klass_names = [klass.__name__ for klass in klasses]
        self.assertTrue("SampleFactor" in klass_names)

    def test_subfactors(self):
        klasses = subclasses_in_package(FactorNode, 'test_extensions')
        klass_names = [klass.__name__ for klass in klasses]
        self.assertTrue("SampleFactor" in klass_names)
        self.assertTrue("AnotherFactor" in klass_names)
        self.assertFalse("FactorNode" in klass_names)
        # if klass.__doc__:
        #     print klass.__doc__

    def test_get_factor_info(self):
        info = get_factor_extensions()
        # TODO: define the structure for this info
        print(info)

if __name__ == '__main__':
    unittest.main()
