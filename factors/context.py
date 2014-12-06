from factors.nodes import Node
class Context(object):

    def __init__(self):
        # Mapping from node_id to Node
        self._nodes = dict()

    def add_node(self, node):
        self._nodes[node.id] = node

    def remove_node(self, node_id):
        self._nodes.pop(node_id,None)

    def resolve_uri(self, uri):
        node_id = Node.id_from_uri(uri)
        terminal_name = Node.terminal_name_from_uri(uri)
        node = self._nodes[node_id]
        return node.get_terminal(terminal_name)
