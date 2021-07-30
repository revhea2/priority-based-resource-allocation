from models.application import Application
from models.node import Node
from models.program import Program
from resource_allocation import ResourceAllocation
from resource_handler import ResourceHandler
from dispatcher import Dispatcher
from objective_function import ObjectiveFunction


def release_resources(_type, value, req_node):
    # todo: naming for value

    if _type == 1:
        for node in nodes:
            if req_node.node_id == node.node_id:
                node.disk_space += value.disk_size
                return
    elif _type == 2:
        for node in nodes:
            if req_node.node_id == node.node_id:
                node.program_shareability += 1
                node.memory_size += value.memory_size
                return


def node_selection(_type, request):
    if _type == 1:
        max_size = 0
        max_node = None
        for node in nodes:
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

    elif _type == 2:
        selected_nodes = []
        for program in request:
            max_size = 0
            max_node = None
            for node in nodes:
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
        for node in nodes:
            if node.printers >= request:
                node.printers -= request
                return node
        return None


def resource_allocation_algorithm1(Pool, allocated, allocation_queue, unallocated):
    for i in range(len(Pool)):
        for j in range(len(Pool[i])):
            app = Pool[i][j]
            disk_node = None
            selected_nodes = None
            # checks the disk size
            if app.disk_size > 0:
                disk_node = node_selection(1, app.disk_size)
                if not disk_node:
                    unallocated[i].append(app)
                    continue

            # checks if program exist in the node
            if app.programs:

                selected_nodes = node_selection(2, app.programs)
                if not selected_nodes:
                    # todo: release resources
                    release_resources(1, app, disk_node)
                    unallocated[i].append(app)
                    continue
                if len(selected_nodes) != len(app.programs):
                    release_resources(1, app, disk_node)
                    for node in selected_nodes:
                        prg, prg_node = node
                        release_resources(2, prg, prg_node)
                    unallocated[i].append(app)
                    continue

            if app.printers > 0:
                printer_node = node_selection(3, app.printers)

                if not printer_node:
                    release_resources(1, app, disk_node)
                    for node in selected_nodes:
                        prg, prg_node = node
                        release_resources(2, prg, prg_node)
                    unallocated[i].append(app)
                    continue

            print(f"Resources changed: application id: {app.app_id}")
            for node in nodes:
                print(node)
            allocated.append(app)

    print("Unallocated: ", unallocated)
    return allocated


# todo: algo 2 for resource alloc
def resource_allocation_algorithm2(Pool, allocated, allocation_queue):
    unallocated = [[] for _ in range(len(Pool))]
    resource_allocation_algorithm1(Pool, allocated, allocation_queue, unallocated)

    # for p in Pool:
    #     unallocated = []
    #     if p:
    #
    #     else:


def initialize_programs(_programs):
    _programs.append(Program(1, "Windows Shell", 1))
    _programs.append(Program(2, "Pycharm", 1.5))
    _programs.append(Program(3, "Microsoft Office", 0.5))


def initialize_nodes(_nodes):
    _nodes.append(
        Node(node_id=1, disk_space=40, memory_size=16, printers=0, resident_program=None, program_shareability=0))
    _nodes.append(
        Node(node_id=2, disk_space=20, memory_size=4, printers=1, resident_program=programs[2], program_shareability=2))
    _nodes.append(
        Node(node_id=3, disk_space=4, memory_size=64, printers=0, resident_program=programs[0], program_shareability=3))
    _nodes.append(
        Node(node_id=4, disk_space=10, memory_size=32, printers=1, resident_program=programs[1],
             program_shareability=4))
    _nodes.append(
        Node(node_id=5, disk_space=30, memory_size=8, printers=0, resident_program=programs[0], program_shareability=1))


def initialize_apps(_apps):
    p1 = programs[0]
    p1.number = 1
    p2 = programs[2]
    p2.number = 1
    _apps.append(Application(1, "App1", 5, [p1, p2], 1))

    p1 = programs[1]
    p1.number = 1

    _apps.append(Application(2, "App2", 8, [p1], 1))
    _apps.append(Application(3, "App3", 2, printers=1))


if __name__ == '__main__':

    # initialize programs
    programs = []
    initialize_programs(programs)

    # initialize nodes
    nodes = []
    initialize_nodes(nodes)

    # initialize resource handler/table
    resource_table = ResourceHandler(programs, nodes)
    resource_table.view_resources_table()

    # initialize apps
    apps = []
    initialize_apps(apps)

    # initialize dispatcher
    dispatcher = Dispatcher()
    # initialize  objective function
    of = ObjectiveFunction(resource_table)

    # perform dispatching
    pool = dispatcher.dispatch(apps, programs, len(programs) + 2, resource_table)

    # perform objective function
    of.objective_function(pool)

    # pool complement
    unalloc = [[] for _ in range(len(pool))]

    resource_allocator = ResourceAllocation(pool, resource_table)
    resource_allocator.perform_resource_allocation()



