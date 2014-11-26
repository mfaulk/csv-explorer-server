__author__ = 'mfaulk'

from collections import defaultdict
from itertools import chain
from copy import copy
import json as JSON
from factors.nodes import SourceNode, FactorNode, ReportNode, DirectedEdge


class FactorGraph(object):

    def __init__(self):
        self.sourceNodes = set()
        self.factorNodes = set()
        self.reportNodes = set()
        # _edges[node.id] contains a list of edges directed out from node
        self._edges = defaultdict(list)

    def addSourceNode(self, srcNode):
        assert isinstance(srcNode, SourceNode)
        self.sourceNodes.add(srcNode)
        self.compute()

    def addFactorNode(self, factorNode):
        assert isinstance(factorNode, FactorNode)
        self.factorNodes.add(factorNode)
        self.compute()

    def addReportNode(self, reportNode):
        assert isinstance(reportNode, ReportNode)
        self.reportNodes.add(reportNode)
        self.compute()

    def addEdge(self, edge):
        assert isinstance(edge, DirectedEdge)
        assert(not isinstance(edge.dest, SourceNode))
        self._edges[edge.src.id].append(edge)
        self.compute()

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
        node_ids.extend(map(lambda n: str(n.id), self.sourceNodes))
        node_ids.extend(map(lambda n: str(n.id), self.factorNodes))
        node_ids.extend(map(lambda n: str(n.id), self.reportNodes))

        edge_list = map(lambda e: {'src': str(e.src.id), 'dst': str(e.dest.id)}, self.get_edges())

        temp_dict = dict()
        temp_dict['nodes'] = node_ids
        temp_dict['edges'] = edge_list
        return JSON.dumps(temp_dict)


    def nodes_to_json(self):

        src_info = list()
        for node in self.sourceNodes:
            info = dict()
            info['id'] = str(node.id)
            info['name'] = node.name
            info['type'] = node.__class__.__name__
            src_info.append(info)

        factor_info = list()
        for node in self.factorNodes:
            info = dict()
            info['id'] = str(node.id)
            info['name'] = node.name
            info['type'] = node.__class__.__name__
            factor_info.append(info)

        report_info = list()
        for node in self.reportNodes:
            info = dict()
            info['id'] = str(node.id)
            info['name'] = node.name
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
        roots.extend(self.sourceNodes)
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

