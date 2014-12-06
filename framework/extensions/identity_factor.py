import pandas as pd
from factors.nodes import Node, FactorNode

class IdentityFactor(FactorNode):

    def __init__(self, context, args):
        '''

        :param input_uris: list of URIs
        :param context: Context object
        :return:
        '''
        super(IdentityFactor,self).__init__()
        self.input_uris = args['input_uris']
        # resolve URIs and construct a dataframe
        self._load_df(context)

    def _load_df(self, context):
        d = dict()
        for uri in self.input_uris:
            series = context.resolve_uri(uri)
            terminal_name = Node.terminal_name_from_uri(uri)
            d[terminal_name] = series
        self.df = pd.DataFrame(d)


    def describe_output_terminals(self):
        '''

        :return: A dict mapping output terminal names to their data types
        '''
        #return self.df.to_dict()
        #return self.df.columns.tolist()
        return [self.to_uri(terminal_name) for terminal_name in self.df.columns.tolist()]

    def get_terminal(self, terminal_name):
        if terminal_name in list(self.df.columns):
            return self.df[terminal_name].copy(deep=True)

    # @staticmethod
    # def describe_input_terminals():
    #     '''
    #
    #     :return: A list of 'terminals' represented as dicts
    #     '''
    #     terminal_name = "INPUT"
    #     inputs = [Node._terminal(terminal_name, Node.TYPE_STRING)]
    #     return inputs
    #
    # @staticmethod
    # def describe_output_terminals():
    #     '''
    #
    #     :return: A dict mapping output terminal names to their data types
    #     '''
    #     terminal_name = "OUTPUT"
    #     output_terminals = [Node._terminal(terminal_name, Node.TYPE_STRING)]
    #     return output_terminals


    def compute(self):
        '''
        Evaluate this factor.
        :return:
        '''
        pass