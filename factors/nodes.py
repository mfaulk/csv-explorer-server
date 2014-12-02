from models import Table
import uuid

class Node(object):
    ''' A node in the factor graph.
    '''
    def __init__(self):
        self.id = uuid.uuid4()

class SourceNode(Node):
    ''' An initial data source. It may not have parents.
    '''

    def __init__(self):
        '''
        Init a node for a data source.
        '''
        super(SourceNode,self).__init__()

    def describe_output_terminals(self):
        '''

        :return: A dict mapping output terminal names to their data types
        '''
        return dict()

    def compute(self):
        pass


class FactorNode(Node):
    ''' A derived data source. This should be an abstract class
    '''

    def __init__(self):
        super(FactorNode,self).__init__()

    def describe_input_terminals(self):
        '''

        :return: A dict mapping input terminal names to their data types
        '''
        return dict()


    def describe_output_terminals(self):
        '''

        :return: A dict mapping output terminal names to their data types
        '''
        return dict()


    def compute(self):
        '''
        Evaluate this factor.
        :return:
        '''
        pass


class ReportNode(Node):
    ''' A derived product that does not persist data.
    '''

    def __init__(self, name="ReportNode"):
        self.name = name
        super(ReportNode,self).__init__()

    def compute(self):
        '''
        Evaluate this report.
        '''
        pass


class DirectedEdge(object):
    ''' A directed edge between two Nodes.
    '''


    def __init__(self, src, dest):
        '''
        :param srcNode: instance of Node
        :param destNode: instance of Node
        '''
        self.src = src
        self.dest = dest