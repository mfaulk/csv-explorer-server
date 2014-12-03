__author__ = 'mfaulk'

from collections import defaultdict
from itertools import chain
from copy import copy
import json as JSON
from factors.nodes import Node, SourceNode, FactorNode, ReportNode, DirectedEdge
import factors.node_factory


class FactorGraph(object):

    def __init__(self):
        self.sourceNodes = dict()
        self.factorNodes = dict()
        self.reportNodes = dict()
        # _edges[node.id] contains a list of edges directed out from node
        self._edges = defaultdict(list)

    def addNode(self, class_name, extensions_path="framework.extensions"):
        node = factors.node_factory.get_instance(class_name, extensions_path)
        assert isinstance(node, Node)
        if isinstance(node, SourceNode):
            self.sourceNodes[node.id] = node
        elif isinstance(node, FactorNode):
            self.factorNodes[node.id] = node
        elif isinstance(node, ReportNode):
            self.reportNodes[node.id] = node
        else:
            print("Unknown node type " + node.__class__)
        self.compute()
        return node.id

    def addSourceNode(self, srcNode):
        assert isinstance(srcNode, SourceNode)
        self.sourceNodes[srcNode.id] = srcNode
        self.compute()

    def addFactorNode(self, factorNode):
        assert isinstance(factorNode, FactorNode)
        self.factorNodes[factorNode.id] = factorNode
        self.compute()

    def addReportNode(self, reportNode):
        assert isinstance(reportNode, ReportNode)
        self.reportNodes[reportNode.id] = reportNode
        self.compute()

    def addEdge(self, edge):
        assert isinstance(edge, DirectedEdge)
        assert(not isinstance(edge.dest, SourceNode))
        self._edges[edge.src.id].append(edge)
        self.compute()

    def createEdge(self, src_uri, dest_uri):
        # validate uris: valid nodes, valid terminals, valid input/output
        src_id = Node.id_from_uri(src_uri)
        src_terminal = Node.terminal_name_from_uri(src_uri)
        dest_id = Node.id_from_uri(dest_uri)
        dest_terminal = Node.terminal_name_from_uri(dest_uri)
        pass

    def get_edges(self):
        return list(chain(*self._edges.values()))

    def compute(self):
        # TODO: do this efficiently with dirty bits
        topo_sort = self.topological_sort()
        for node in topo_sort:
            #print node.name
            node.compute()

    def to_json(self):
        node_ids = list()
        node_ids.extend(map(lambda n: str(n.id), self.sourceNodes.values()))
        node_ids.extend(map(lambda n: str(n.id), self.factorNodes.values()))
        node_ids.extend(map(lambda n: str(n.id), self.reportNodes.values()))

        edge_list = map(lambda e: {'src': str(e.src.id), 'dst': str(e.dest.id)}, self.get_edges())

        temp_dict = dict()
        temp_dict['nodes'] = node_ids
        temp_dict['edges'] = edge_list
        return JSON.dumps(temp_dict)


    def nodes_to_json(self):

        src_info = list()
        for node in self.sourceNodes.values():
            info = dict()
            info['id'] = str(node.id)
            info['type'] = node.__class__.__name__
            src_info.append(info)

        factor_info = list()
        for node in self.factorNodes.values():
            info = dict()
            info['id'] = str(node.id)
            info['type'] = node.__class__.__name__
            factor_info.append(info)

        report_info = list()
        for node in self.reportNodes.values():
            info = dict()
            info['id'] = str(node.id)
            info['type'] = node.__class__.__name__
            report_info.append(info)

        return JSON.dumps({"sources": src_info, "factors": factor_info, "reports": report_info})


    def topological_sort(self):
        ''' A topological sorting of the factor graph.
        :return: list of nodes in topological order
        '''
        edges = copy(self._edges)
        topo_sort = list()
        # Set of nodes with no incoming edges
        roots = list()
        roots.extend(self.sourceNodes.values())
        while roots:
            node = roots.pop()
            topo_sort.append(node)
            out_edges = edges.pop(node.id, list())
            children = map(lambda e: e.dest, out_edges)
            for child in children:
                # if child has no remaining incoming edges, append it to roots
                # TODO: do this efficiently
                is_root = True
                for edge in list(chain(*edges.values())):
                    if(edge.dest == child):
                        is_root = False
                        break
                if is_root:
                    roots.append(child)
        return topo_sort

