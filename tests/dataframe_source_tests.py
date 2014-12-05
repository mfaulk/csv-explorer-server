import unittest
import pandas as pd
from pandas import Series
from framework.extensions.dataframe_source import DataframeSource

class DataframeSourceTests(unittest.TestCase):

    def setUp(self):
        self.df1 = pd.DataFrame({
            'A': 1.,
            'B': pd.Timestamp('20130102'),
            'C': pd.Series(1,index=list(range(4)),dtype='float32'),
            'D': pd.Categorical(["test","train","test","train"]),
            'E': 'foo'})

    def test_df(self):
        node = DataframeSource(self.df1)

        A = node.get_terminal("A")
        self.assertTrue(isinstance(A, Series))
        self.assertEqual(len(A.tolist()), 4)
        self.assertEqual(A[2], 1)

        E = node.get_terminal("E")
        self.assertEqual(E[0], 'foo')

    def test_describe_terminals(self):
        node = DataframeSource(self.df1)
        terminals = node.describe_output_terminals()
        expected_terminals = set(["A", "B", "C", "D", "E"])
        self.assertEqual(expected_terminals, set(terminals.keys()))