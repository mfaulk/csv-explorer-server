from collections import defaultdict
from itertools import chain
from copy import copy
import json as JSON
from uuid import UUID
from factors.nodes import Node, SourceNode, FactorNode, TerminalEdge
import factors.node_factory
from factors.context import Context


class FactorGraph(object):

    def __init__(self):
        # Mapping from node ID to Node object
        self._nodes = dict()
        # Mapping from node ID to its incident edges
        self._edges = defaultdict(list)

        self._edges_by_id = dict()
        self._context = Context()


    def add_node(self, class_name, extensions_path="framework.extensions", args=None):
        '''
        :param class_name:
        :param extensions_path:
        :return:
        '''
        node = factors.node_factory.get_instance(class_name, self._context, extensions_path=extensions_path, args=args)
        assert isinstance(node, Node)
        self._nodes[node.id] = node
        self._context.add_node(node)
        #self.compute()
        return node.id

    def delete_node(self, node_id):
        node = self._nodes.pop(node_id, None)
        self._context.remove_node(node)
        # delete all edges incident on this node
        edges = self._edges.pop(node_id, list())
        for edge in edges:
            self.delete_edge(edge)

    def add_edge(self, src_uri, dest_uri):
        src_id = Node.id_from_uri(src_uri)
        dest_id = Node.id_from_uri(dest_uri)
        edge_id = None
        if src_id in self._nodes and dest_id in self._nodes:
            edge = TerminalEdge(src_uri, dest_uri)
            self._edges[src_id].append(edge)
            self._edges[dest_id].append(edge)
            self._edges_by_id[edge.id] = edge
            edge_id = edge.id
        else:
            print("Unknown node(s). src_id: " + src_id + ", dest_id: " + dest_id)
        return edge_id

    def delete_edge_by_id(self, edge_id):
        if edge_id in self._edges_by_id:
            edge = self._edges_by_id.pop(edge_id)
            self.delete_edge(edge)

    def delete_edge(self, edge):
        src_id = edge.src_id
        dest_id = edge.dest_id
        if edge in self._edges[src_id]:
            self._edges[src_id].remove(edge)
        if edge in self._edges[dest_id]:
            self._edges[dest_id].remove(edge)

    def get_edges(self):
        return set(chain(*self._edges.values()))

    def get_edge(self, edge_id):
        edge = None
        if edge_id in self._edges_by_id:
            edge = self._edges_by_id[edge_id]
        return edge

    @staticmethod
    def _children(parent_id, edges):
        '''
        :param parent_id: id of node
        :return: set of child ids
        '''
        incident_edges = edges[parent_id]
        #return set([Node.id_from_uri(edge.dest) for edge in incident_edges if Node.id_from_uri(edge.src) == parent_id])
        return set([edge.dest_id for edge in incident_edges if edge.src_id == parent_id])

    def compute(self):
        # TODO: do this efficiently with dirty bits
        topo_sort = self.topological_sort(self._nodes, self._edges)
        for node_id in topo_sort:
            self._nodes[node_id].compute()

    def to_json(self):
        edge_list = map(lambda e: {'src': e.src_uri, 'dst': e.dest_uri}, self.get_edges())
        temp_dict = dict()
        temp_dict['nodes'] = self._nodes.keys()
        temp_dict['edges'] = edge_list
        return JSON.dumps(temp_dict)

    def _describe_node(self, node_id):
        info = dict()
        if node_id in self._nodes:
            node = self._nodes[node_id]
            info = dict()
            info['id'] = str(node.id)
            info['type'] = node.__class__.__name__
            if isinstance(node, SourceNode):
                info['outputs'] = node.describe_output_terminals()
            elif isinstance(node, FactorNode):
                info['inputs'] = node.describe_input_terminals()
                info['outputs'] = node.describe_output_terminals()
            else:
                print(self.__class__.__name__ + ": Unknown node type " + node.__class__.__name__)
        return info

    def nodes_to_json(self):
        data = list()
        for node_id in self._nodes.keys():
            info = self._describe_node(node_id)
            data.append(info)

        return JSON.dumps({"nodes": data})

    def node_to_json(self, node_id):
        info = self._describe_node(node_id)
        return JSON.dumps(info)

    @staticmethod
    def topological_sort(nodes, edges):
        ''' A topological sorting of the factor graph.
        :return: list of node ids in topological order
        '''
        nodes = copy(nodes)
        edges = copy(edges)
        topo_sort = list()
        # Set of nodes with no incoming edges
        roots = set([id for (id,node) in nodes.iteritems() if isinstance(node, SourceNode)])
        while roots:
            node_id = roots.pop()
            topo_sort.append(node_id)
            # Delete all edges out from this node. This may cause new roots; if so, append them.
            out_edges = edges.pop(node_id, list())
            for edge in out_edges:
                child_id = edge.dest_id
                if edge in edges[child_id]:
                    edges[child_id].remove(edge)
                    # If all remaining edges incident on this child are out edges, it is a new root.
                    child_out_edges = [edge for edge in edges[child_id] if edge.src_id == child_id]
                    if len(edges[child_id]) == len(child_out_edges) :
                        roots.add(child_id)
                else:
                    print("Edge not found!")
        return topo_sort




