__author__ = 'mfaulk'

from factors.nodes import FactorNode

class AnotherFactor (FactorNode):
    '''
    This docstring declares type(s) of data read by this factor, the type(s) of data written, and where data is written to.

        READS:STRING,STRING
        WRITES:INT
        WRITESTO:SAMPLE_TABLE
        PARAMETERS:
    '''

    def __init__(self, context, args=None):

        super(AnotherFactor,self).__init__()

    def compute(self):
        '''
        Evaluate this factor.
        :return:
        '''
        print("AnotherFactor.compute")
    pass