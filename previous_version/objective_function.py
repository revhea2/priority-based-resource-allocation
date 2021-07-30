class ObjectiveFunction:

    def __init__(self, nodes):
        self.nodes = nodes
        self.total_node_disk_space = 0
        self.nodes_printer = 0
        for node in nodes:
            self.total_node_disk_space += node.disk_space

        for node in nodes:
            self.nodes_printer += node.printers

    def get_total_program(self, program):
        node_prg = 0

        for node in self.nodes:
            if node.resident_program and node.resident_program == program:
                node_prg += node.program_shareability

        return node_prg

    def get_total_memory(self, program):
        node_memory = 0

        for node in self.nodes:
            if node.resident_program and node.resident_program == program:
                node_memory += node.memory_size

        return node_memory

    def calculate_cost(self, app):
        z = 0

        # for hard disk
        z += app.disk_size / self.total_node_disk_space

        for program in app.programs:
            # for main memory
            z += program.number * program.memory_size / self.get_total_memory(program)

            # for resident programs
            z += program.number / self.get_total_program(program)
        # for printers
        z += app.printers / self.nodes_printer
        print(f"Application id: {app.app_id} cost: {z}")
        return z

    def objective_function(self, pool):

        print("Objective Function: ")
        for apps in pool:
            apps.sort(key=lambda x: self.calculate_cost(x))
