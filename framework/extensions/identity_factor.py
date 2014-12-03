from factors.nodes import Node, FactorNode

class IdentityFactor(FactorNode):

    def __init__(self):
        super(IdentityFactor,self).__init__()

    @staticmethod
    def describe_input_terminals():
        '''

        :return: A list of 'terminals' represented as dicts
        '''
        terminal_name = "INPUT"
        inputs = [Node._terminal(terminal_name, Node.TYPE_STRING)]
        return inputs

    @staticmethod
    def describe_output_terminals():
        '''

        :return: A dict mapping output terminal names to their data types
        '''
        terminal_name = "OUTPUT"
        output_terminals = [Node._terminal(terminal_name, Node.TYPE_STRING)]
        return output_terminals


    def compute(self):
        '''
        Evaluate this factor.
        :return:
        '''
        pass