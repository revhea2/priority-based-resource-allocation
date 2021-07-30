from node_selector import NodeSelector


class ResourceAllocation:

    def __init__(self, pool, resources):
        self.pool = pool
        self.resources = resources

    def resource_deallocate(self, resource_type, allocated_node, selected_node):
        if resource_type == 1:
            self.resources.nodes[selected_node.node_id].disk_space += allocated_node.disk_size
        elif resource_type == 2:
            self.resources.nodes[selected_node.node_id].memory_size += allocated_node.memory_size

    def resource_allocation_algorithm1(self, allocated, allocation_queue, unallocated, node_selector):

        for i in range(len(self.pool)):
            for j in range(len(self.pool[i])):
                app = self.pool[i][j]
                node_for_disk = None
                nodes_for_programs = None

                # check if it requires disk
                if app.disk_size > 0:
                    node_for_disk = node_selector.select(1, app.disk_size)
                    if not node_for_disk:
                        unallocated[i].append(app)
                        continue

                # checks if program exist in the node
                if app.programs:
                    nodes_for_programs = node_selector.select(2, app.programs)
                    if not nodes_for_programs:
                        self.resource_deallocate(1, app, node_for_disk)
                        unallocated[i].append(app)
                        continue
                    if len(nodes_for_programs) < len(app.programs):
                        self.resource_deallocate(1, app, node_for_disk)
                        for node in nodes_for_programs:
                            prg, prg_node = node
                            self.resource_deallocate(2, prg, prg_node)
                        unallocated[i].append(app)
                        continue
                if app.printers > 0:
                    printer_node = node_selector.select(3, app.printers)
                    if not printer_node:
                        self.resource_deallocate(1, app, node_for_disk)
                        for node in nodes_for_programs:
                            prg, prg_node = node
                            self.resource_deallocate(2, prg, prg_node)
                        unallocated[i].append(app)
                        continue
                allocated.append(app)
                print(app, "is allocated!")
                self.resources.view_resources_table()

        allocation_queue.extend(allocated)

    def perform_resource_allocation(self):
        print("Currently in Resource Allocation:")
        node_selector = NodeSelector(self.resources)

        unallocated = [[] for _ in range(len(self.pool))]
        allocated = []
        allocation_queue = []

        self.resource_allocation_algorithm2(allocated, allocation_queue, unallocated, node_selector)

    def resource_allocation_algorithm2(self, allocated, allocation_queue, unallocated, node_selector):
        self.resource_allocation_algorithm1(allocated, allocation_queue, unallocated, node_selector)
