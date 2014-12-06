from factors.nodes import SourceNode

class DataframeSource(SourceNode):
    def __init__(self, context, args):
        self.df = args['df']
        super(SourceNode,self).__init__()

    def describe_output_terminals(self):
        '''

        :return: A list of terminal URIs
        '''
        #return self.df.to_dict()
        return [self.to_uri(terminal_name) for terminal_name in self.df.columns.tolist()]

    def compute(self):
        '''

        :return:
        '''
        pass

    def get_terminal(self, terminal_name):
        if terminal_name in list(self.df.columns):
            return self.df[terminal_name].copy(deep=True)