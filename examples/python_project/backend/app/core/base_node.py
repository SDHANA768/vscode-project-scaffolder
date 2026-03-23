class BaseNode:
    """Base class for all node types"""
    def __init__(self, node_id, name):
        self.node_id = node_id
        self.name    = name
        self.inputs  = []
        self.outputs = []

    def execute(self):
        raise NotImplementedError
