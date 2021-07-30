from models.application import Application
from models.node import Node
from models.program import Program
from resource_allocation import ResourceAllocation
from resource_handler import ResourceHandler
from dispatcher import Dispatcher
from objective_function import ObjectiveFunction

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



