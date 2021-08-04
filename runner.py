from models.application import Application
from models.node import Node
from models.program import Program
from resource_allocation import ResourceAllocation
from resource_handler import ResourceHandler
from dispatcher import Dispatcher
from objective_function import ObjectiveFunction
import random


def initialize_programs(_programs):
    _programs.append(Program(1, "Windows Shell", 1))
    _programs.append(Program(2, "Pycharm", 1.5))
    _programs.append(Program(3, "Microsoft Office", 0.5))


def initialize_nodes(_nodes):
    _nodes.append(
        Node(node_id=1, disk_space=40, memory_size=16, printers=0, resident_program=None, program_shareability=0,
             disk_band=8, printer_band=2))
    _nodes.append(
        Node(node_id=2, disk_space=20, memory_size=4, printers=1, resident_program=programs[2], program_shareability=2,
             disk_band=10, printer_band=1))
    _nodes.append(
        Node(node_id=3, disk_space=5, memory_size=64, printers=0, resident_program=programs[0], program_shareability=3,
             disk_band=17, printer_band=2))
    _nodes.append(
        Node(node_id=4, disk_space=10, memory_size=32, printers=1, resident_program=programs[1],
             program_shareability=4, disk_band=9, printer_band=1))
    _nodes.append(
        Node(node_id=5, disk_space=30, memory_size=8, printers=0, resident_program=programs[0], program_shareability=1,
             disk_band=12, printer_band=1))


def random_app_initialization(_apps, n):
    for i in range(n):
        p_size = random.randint(0, 3)
        prg = []

        for a in range(p_size):
            prg.append(programs[a])

        _apps.append(Application(i + 1, f"App{i + 1}", random.randint(5, 30), prg, random.randint(0, 1)))

    for a in _apps:
        print(a, a.disk_size, a.programs, a.printers)


def view_apps(_apps):
    # Amount to justify the titles/other cells
    justify_amount = 15
    table = "Application TABLE\n"
    # Justify the titles + justify the 5 nodes = 6 * justify amount
    table += f"{'-' * (justify_amount * 7)}\n"

    table += "App id:".ljust(justify_amount, ' ')
    for app in _apps:
        table += f"{app.app_id}".rjust(justify_amount, ' ')
    table += "\n"
    table += f"{'-' * (justify_amount * 7)}\n"
    table += "Hard disk:".ljust(justify_amount, ' ')
    for app in _apps:
        table += f"{app.disk_size}".rjust(justify_amount, ' ')
    table += "\n"
    table += "Programs:".ljust(justify_amount, ' ')
    for app in _apps:
        program_list = [p.program_id for p in app.programs]
        table += f"{program_list}".rjust(justify_amount, ' ')
    table += "\n"
    table += "Printer:".ljust(justify_amount, ' ')
    for app in _apps:
        table += f"{app.printers}".rjust(justify_amount, ' ')
    table += "\n"

    print(table)
    print()


def initialize_apps(_apps):
    p1 = programs[0]
    p2 = programs[1]
    p3 = programs[2]

    _apps.append(Application(1, "App1", 5, [p1, p3], 1))
    _apps.append(Application(2, "App2", 25, [p1, p2], 1))
    _apps.append(Application(3, "App3", 13, [p2, p3], 0))
    _apps.append(Application(4, "App4", 24, [], 1))
    _apps.append(Application(5, "App5", 14, [], 0))
    _apps.append(Application(6, "App6", 30, [p2, p3], 1))

    view_apps(_apps)


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

    is_analysis = False

    if is_analysis:
        random_app_initialization(apps, 500)
    else:
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
    allocation_queue = resource_allocator.perform_resource_allocation()

    print(allocation_queue)
