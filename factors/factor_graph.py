__author__ = 'mfaulk'

from factors.nodes import SourceNode, FactorNode, ReportNode, DirectedEdge
from collections import defaultdict
from itertools import chain
from copy import deepcopy

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
        # TODO: recompute the factor graph...
        pass

    def topological_sort(self):
        ''' A topological sorting of the factor graph.
        :return: list of nodes in topological order
        '''
        edges = deepcopy(self._edges)
        topo_sort = list()
        # Set of nodes with no incoming edges
        roots = list()
        roots.extend(self.sourceNodes)
        while roots:
            node = roots.pop()

            print("Evaluating " + node.name)
            topo_sort.append(node)
            out_edges = edges.pop(node.id, list())
            children = map(lambda e: e.dest, out_edges)
            for child in children:
                print("  Child: " + child.name)
                # if child has no remaining incoming edges, append it to roots
                # TODO: do this efficiently
                is_root = True
                for edge in list(chain(*edges.values())):
                    print(type(edge))
                    if(edge.dest == child):
                        is_root = False
                        break
                if is_root:
                    roots.append(child)
        return topo_sort