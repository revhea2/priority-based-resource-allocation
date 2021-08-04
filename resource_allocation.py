from node_selector import NodeSelector
from variant_diskstras_algorithm import VDA


class ResourceAllocation:

    def __init__(self, pool, resources):
        self.pool = pool
        self.resources = resources
        self.vda = VDA(None)

    def resource_deallocate(self, resource_type, allocated_node, selected_node):
        if resource_type == 1:
            self.resources.nodes[selected_node.node_id].disk_space += allocated_node.disk_size
        elif resource_type == 2:
            self.resources.nodes[selected_node.node_id].memory_size += allocated_node.memory_size
            self.resources.nodes[selected_node.node_id].program_shareability += 1
        else:
            self.resources.nodes[selected_node.node_id].printers += allocated_node.printers

    def check_path(self, path):
        for index in range(1, len(path)):
            if self.vda.check_bandwidth(path[index]) == 0:
                return False
        return True

    def resource_allocation_algorithm1(self, allocated, allocation_queue, unallocated, node_selector):
        print("Resource allocation algorithm   - - - -  - -  - - - - -  - -  - - - - ")
        newly_allocated = []
        for i in range(len(self.pool)):
            for j in range(len(self.pool[i])):
                app = self.pool[i][j]
                print(app)
                node_for_disk = None
                nodes_for_programs = None
                node_for_printer = None

                print("Before VDA: ")
                self.vda.view_graph()

                allocated_bandwidths = {}
                allocated_resources = {}

                """
                NODE SELECTION ***********************************************************************************
                """

                # check if it requires disk
                if app.disk_size > 0:
                    node_for_disk = node_selector.select(1, app.disk_size)
                    if not node_for_disk:
                        unallocated[i].append(app)
                        continue
                    allocated_resources[1] = node_for_disk

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
                    allocated_resources[2] = nodes_for_programs

                if app.printers > 0:
                    node_for_printer = node_selector.select(3, app.printers)
                    if not node_for_printer:
                        if node_for_disk:
                            self.resource_deallocate(1, app, node_for_disk)
                        if nodes_for_programs:
                            for node in nodes_for_programs:
                                prg, prg_node = node
                                self.resource_deallocate(2, prg, prg_node)
                        unallocated[i].append(app)

                        continue
                    allocated_resources[3] = node_for_printer

                """
                       VARIANT DIJKSTRA'S ALGORITHM *******************************************************
                """

                paths = self.vda.variant_dijkstra_algorithm(0, len(self.resources.nodes) + 1)
                has_enough_bandwidth = 0

                if node_for_disk and node_for_printer:
                    bandwidth_types = 2
                elif node_for_disk or node_for_printer:
                    bandwidth_types = 1
                else:
                    bandwidth_types = 0

                """
                            BANDWIDTH SELECTION *******************************************************
                            check if the paths with max bandwidths are enough to accommodate the requested bandwidth
                """

                quality_of_service = 0.5

                # check disk_size_path
                if node_for_disk and self.check_path(paths[node_for_disk.node_id]):
                    has_enough_bandwidth += 1

                if node_for_printer and self.check_path(paths[node_for_printer.node_id]):
                    has_enough_bandwidth += 1

                if has_enough_bandwidth != bandwidth_types:
                    # deallocate
                    self.resource_deallocate(1, app, node_for_disk)
                    if nodes_for_programs:
                        for node in nodes_for_programs:
                            prg, prg_node = node
                            self.resource_deallocate(2, prg, prg_node)
                    if node_for_printer:
                        self.resource_deallocate(3, app, node_for_printer)
                    unallocated[i].append(app)
                    continue

                if node_for_disk:

                    if self.vda.check_bandwidth(node_for_disk.node_id) < node_for_disk.disk_band * quality_of_service:

                        # deallocate
                        self.resource_deallocate(1, app, node_for_disk)
                        if nodes_for_programs:
                            for node in nodes_for_programs:
                                prg, prg_node = node
                                self.resource_deallocate(2, prg, prg_node)
                        if node_for_printer:
                            self.resource_deallocate(3, app, node_for_printer)

                        unallocated[i].append(app)
                        continue
                    else:

                        available = self.vda.check_bandwidth(node_for_disk.node_id)
                        allocated_band = available if available < node_for_disk.disk_band else node_for_disk.disk_band
                        self.vda.allocate_band(node_for_disk.node_id, allocated_band)
                        allocated_bandwidths[1] = [node_for_disk, self.vda.pre[node_for_disk.node_id], allocated_band]

                # for printer bandwidth
                if node_for_printer:
                    if self.vda.check_bandwidth(
                            node_for_printer.node_id) < node_for_printer.printer_band * quality_of_service:
                        # deallocate
                        self.resource_deallocate(1, app, node_for_disk)
                        if nodes_for_programs:
                            for node in nodes_for_programs:
                                prg, prg_node = node
                                self.resource_deallocate(2, prg, prg_node)
                        if node_for_printer:
                            self.resource_deallocate(1, app, node_for_printer)
                        unallocated[i].append(app)
                        continue
                    else:
                        available = self.vda.check_bandwidth(node_for_printer.node_id)
                        allocated_band = available if available < node_for_printer.printer_band else node_for_printer.printer_band
                        self.vda.allocate_band(node_for_printer.node_id, allocated_band)
                        allocated_bandwidths[2] = [node_for_printer, self.vda.pre[node_for_printer.node_id],
                                                   allocated_band]

                allocated.append([app, allocated_bandwidths, allocated_resources])
                newly_allocated.append([app])

                # prints details
                print(app, "is allocated!")
                self.resources.view_resources_table()
                self.vda.view_graph()
                print("\n = = = = = = = = = = = = = = = = = = = = = = ")

        allocation_queue.extend(newly_allocated)

    def perform_resource_allocation(self):
        print("Currently in Resource Allocation:")
        node_selector = NodeSelector(self.resources)

        unallocated = [[] for _ in range(len(self.pool))]
        allocated = []
        allocation_queue = []

        self.resource_allocation_algorithm2(allocated, allocation_queue, unallocated, node_selector)

        return allocation_queue

    def resource_allocation_algorithm2(self, allocated, allocation_queue, unallocated, node_selector):

        self.resource_allocation_algorithm1(allocated, allocation_queue, unallocated, node_selector)
        self.pool = unallocated
        unallocated = [[] for _ in range(len(self.pool))]

        if not self.has_no_apps_in_pool():
            if allocated:
                # app with minimum execution time are released
                app, bandwidth_allocations, resource_allocations = allocated.pop(0)
                if 1 in resource_allocations:
                    self.resource_deallocate(1, app, resource_allocations[1])
                if 2 in resource_allocations:
                    for node in resource_allocations[2]:
                        prg, prg_node = node
                        self.resource_deallocate(2, prg, prg_node)
                if 3 in resource_allocations:
                    self.resource_deallocate(3, app, resource_allocations[3])

                if bandwidth_allocations:
                    if 1 in bandwidth_allocations:
                        self.vda.re_allocate_band(bandwidth_allocations[1][0].node_id, bandwidth_allocations[1][1],
                                                  bandwidth_allocations[1][2])
                    if 2 in bandwidth_allocations:
                        self.vda.re_allocate_band(bandwidth_allocations[2][0].node_id, bandwidth_allocations[2][1],
                                                  bandwidth_allocations[2][2])
            self.resource_allocation_algorithm2(allocated, allocation_queue, unallocated, node_selector)

    def has_no_apps_in_pool(self):
        for apps in self.pool:
            if len(apps) > 0:
                return False
        return True
