import unittest
from framework.extensions.identity_factor import IdentityFactor
from factors.nodes import Node

class TerminalTests(unittest.TestCase):

    def test_identity_input_terminals(self):
        terminals = IdentityFactor.describe_input_terminals()
        self.assertTrue(isinstance(terminals, list))
        self.assertEqual(len(terminals),1)
        terminal = terminals[0]
        self.assertEqual(terminal['type'], Node.TYPE_STRING)
        terminal_name = terminal['name']
        self.assertEqual(terminal_name, "INPUT")

    def test_identity_output_terminals(self):
        terminals = IdentityFactor.describe_output_terminals()
        self.assertTrue(isinstance(terminals, list))
        self.assertEqual(len(terminals),1)
        terminal = terminals[0]
        self.assertEqual(terminal['type'], Node.TYPE_STRING)
        terminal_name = terminal['name']
        self.assertEqual(terminal_name, "OUTPUT")

if __name__ == '__main__':
    unittest.main()
