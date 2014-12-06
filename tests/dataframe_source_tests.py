import unittest
import pandas as pd
from pandas import Series
from framework.extensions.dataframe_source import DataframeSource
from factors.nodes import Node
from factors.context import Context

class DataframeSourceTests(unittest.TestCase):

    def setUp(self):
        self.context = Context()
        self.df1 = pd.DataFrame({
            'A': 1.,
            'B': pd.Timestamp('20130102'),
            'C': pd.Series(1,index=list(range(4)),dtype='float32'),
            'D': pd.Categorical(["test","train","test","train"]),
            'E': 'foo'})

    def test_df(self):
        node = DataframeSource(self.context, args={'df': self.df1})

        A = node.get_terminal("A")
        self.assertTrue(isinstance(A, Series))
        self.assertEqual(len(A.tolist()), 4)
        self.assertEqual(A[2], 1)

        E = node.get_terminal("E")
        self.assertEqual(E[0], 'foo')

    def test_describe_terminals(self):
        node = DataframeSource(self.context, args={'df': self.df1})
        terminal_uris = node.describe_output_terminals()
        terminal_names = ["A", "B", "C", "D", "E"]
        expected_terminal_uris = set([Node.to_uri(node, terminal_name) for terminal_name in terminal_names])
        self.assertEqual(expected_terminal_uris, set(terminal_uris))