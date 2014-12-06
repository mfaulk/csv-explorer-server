from models import Table
import uuid
import json
from urlparse import urlparse

class Node(object):
    ''' A node in the factor graph.
    '''

    # Terminal data types
    TYPE_STRING = "STRING"
    TYPE_NUMBER = "NUMBER"

    def __init__(self, context=None, args=None):
        self.id = str(uuid.uuid4())

    def get_terminal(self, terminal_name):
        '''

        :param terminal_name:
        :return: A pandas Series
        '''
        pass


    def to_uri(self, terminal_name):
        # TODO: ensure that terminal name makes a valid URI (no extra slashes, no spaces, ...)
        uri = "node://" + str(self.id) + '/' + terminal_name.upper()
        return uri

    def _terminal_uri(self, terminal_name, data_type):
        return {'uri': self.to_uri(terminal_name), 'type': data_type}

    @staticmethod
    def id_from_uri(uri):
        parse_result = urlparse(uri)
        return parse_result.netloc

    @staticmethod
    def terminal_name_from_uri(uri):
        parse_result = urlparse(uri)
        return parse_result.path.strip('/')

    @staticmethod
    def _terminal(terminal_name, data_type):
        return {'name': terminal_name, 'type': data_type}

class SourceNode(Node):
    ''' An initial data source. It may not have parents.
    '''

    def __init__(self,context=None,args=None):
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
        '''

        :return:
        '''
        pass


class FactorNode(Node):
    ''' A derived data source. This should be an abstract class
    '''

    def __init__(self,context=None, args=None):
        super(FactorNode,self).__init__()

    # @staticmethod
    # def describe_input_terminals():
    #     '''
    #
    #     :return: A dict mapping input terminal names to their data types
    #     '''
    #     return dict()


    def describe_output_terminals(self):
        '''

        :return: A dict mapping output terminal names to their data types
        '''
        return dict()

    def compute(self, context=None):
        '''
        Evaluate this node.
        :param context: a dict mapping this node's input terminal names to source data URIs
        :return:
        '''
        pass


# class ReportNode(Node):
#     ''' A derived product that does not persist data.
#     '''
#
#     def __init__(self):
#         super(ReportNode,self).__init__()
#
#     def compute(self, context=None):
#         '''
#         Evaluate this node.
#         :param context: a dict mapping this node's input terminal names to source data URIs
#         :return:
#         '''
#         pass


class TerminalEdge(object):

    def __init__(self, src_uri, dest_uri):
        '''

        :param src: source URI
        :param dest: dest URI
        :return:
        '''
        self.id = str(uuid.uuid4())
        self.src_uri = src_uri
        self.src_id = Node.id_from_uri(src_uri)
        self.dest_uri = dest_uri
        self.dest_id = Node.id_from_uri(dest_uri)


    def __eq__(self, other):
        return self.src_uri == other.src_uri and self.dest_uri == other.dest_uri

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_json(self):
        return json.dumps({"edge_id": self.id, "src_uri": self.src_uri, "dest_uri": self.dest_uri})