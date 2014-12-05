from factors.nodes import SourceNode

class DataframeSource(SourceNode):
    def __init__(self, df):
        self.df = df
        super(SourceNode,self).__init__()

    def describe_output_terminals(self):
        '''

        :return: A dict mapping output terminal names to their data types
        '''
        return self.df.to_dict()

    def compute(self):
        '''

        :return:
        '''
        pass

    def get_terminal(self, terminal_name):
        if terminal_name in list(self.df.columns):
            return self.df[terminal_name].copy(deep=True)