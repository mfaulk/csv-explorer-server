import unittest
import pandas as pd
from pandas.util.testing import assert_series_equal
from framework.extensions.identity_factor import IdentityFactor
from framework.extensions.dataframe_source import DataframeSource
from factors.nodes import Node
from factors.context import Context


class TerminalTests(unittest.TestCase):

    def setUp(self):
        self.context = Context()
        self.df = pd.DataFrame({
            'A': 1.,
            'B': pd.Timestamp('20130102'),
            'C': pd.Series(1,index=list(range(4)),dtype='float32'),
            'D': pd.Categorical(["test","train","test","train"]),
            'E': 'foo'})
        self.sourceA = DataframeSource(self.context, args={'df': self.df})
        self.context.add_node(self.sourceA)

    def test_identity_factor_terminal_names(self):
        input_uris = self.sourceA.describe_output_terminals()
        args = {'input_uris': input_uris}
        identity = IdentityFactor(self.context, args)
        terminal_names = set([Node.terminal_name_from_uri(uri) for uri in identity.describe_output_terminals()])
        self.assertEqual(terminal_names, set(['A','B','C','D','E']))

    def test_identity_factor_terminal_data(self):
        input_uris = self.sourceA.describe_output_terminals()
        args = {'input_uris': input_uris}
        identity = IdentityFactor(self.context, args)

        for terminal_name in ['A','B','C','D','E']:
            assert_series_equal(self.sourceA.get_terminal(terminal_name), identity.get_terminal(terminal_name))


if __name__ == '__main__':
    unittest.main()
