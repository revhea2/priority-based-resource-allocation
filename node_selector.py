class NodeSelector:

    def __init__(self, resources):
        self.resources = resources

    def select(self, resource_type, request):

        # selects fittest node for disk resource
        if resource_type == 1:
            max_size = 0
            max_node = None
            for node_id, node in self.resources.nodes.items():
                if request == node.disk_space:
                    node.disk_space = 0
                    return node
                elif node.disk_space > request and node.disk_space > max_size:
                    max_node = node
                    max_size = node.disk_space
            if max_size > 0:
                max_node.disk_space -= request
                return max_node
            return None

        # selects the fittest node for each program from the request
        elif resource_type == 2:
            selected_nodes = []
            for program in request:
                max_size = 0
                max_node = None
                # todo: program number should be taken to account
                for node_id, node in self.resources.nodes.items():
                    if node.resident_program and program == node.resident_program:
                        if program.memory_size == node.memory_size:
                            node.memory_size = 0
                            node.program_shareability -= 1
                            selected_nodes.append([program, node])
                            break
                        elif node.memory_size > program.memory_size and node.memory_size > max_size:
                            max_size = node.memory_size
                            max_node = node

                if max_size > 0:
                    max_node.program_shareability -= 1
                    max_node.memory_size -= program.memory_size
                    selected_nodes.append([program, max_node])

            if not selected_nodes:
                return None

            return selected_nodes

        else:
            for node_id, node in self.resources.nodes.items():
                if node.printers >= request:
                    node.printers -= request
                    return node
            return None



    def release(self):
        pass
