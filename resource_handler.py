class ResourceHandler:

    def __init__(self, programs, nodes):
        self.programs = programs
        self.nodes_list = nodes
        self.nodes = {}
        self.total_memory_space = 0
        self.total_disk_space = 0
        self.total_shareability = 0
        self.total_printers = 0
        self.total_program_shareability = 0

        # individual program resources
        self.total_program_share = {}
        self.total_program_memory = {}

        self.set_total_program_resources(programs)

        # add all nodes to the resource table
        for node in nodes:
            self.add_node(node)

    def set_total_program_resources(self, programs):
        for program in programs:
            self.total_program_share[program.program_id] = 0
            self.total_program_memory[program.program_id] = 0

    def add_node(self, node):
        self.nodes[node.node_id] = node
        self.total_memory_space += node.memory_size
        self.total_printers += node.printers
        self.total_disk_space += node.disk_space
        self.total_program_shareability += node.program_shareability
        if node.resident_program:
            self.total_program_share[node.resident_program.program_id] += node.program_shareability
            self.total_program_memory[node.resident_program.program_id] += node.memory_size

    def get_total_disk(self):
        return self.total_disk_space

    def get_total_printers(self):
        return self.total_printers

    def get_total_shareability(self):
        return self.total_program_shareability

    def get_program_total_share(self, program):
        return self.total_program_share[program.program_id]

    def get_program_total_memory(self, program):
        return self.total_program_memory[program.program_id]

    def view_resources_table(self):
        # Amount to justify the titles/other cells
        justify_amount = 15
        table = "RESOURCE TABLE\n"
        # Justify the titles + justify the 5 nodes = 6 * justify amount
        table += f"{'-' * (justify_amount * 6)}\n"

        table += "Node id:".ljust(justify_amount, ' ')
        for node in self.nodes_list:
            table += f"{node.node_id}".rjust(justify_amount, ' ')
        table += "\n"
        table += f"{'-' * (justify_amount * 6)}\n"
        table += "Program id:".ljust(justify_amount, ' ')
        for node in self.nodes_list:
            to_put = f"{node.resident_program.program_id}" if node.resident_program else "-"
            table += f"{to_put}".rjust(justify_amount, ' ')
        table += "\n"
        table += "Prog share no:".ljust(justify_amount, ' ')
        for node in self.nodes_list:
            to_put = f"{node.program_shareability}" if node.resident_program else "-"
            table += f"{to_put}".rjust(justify_amount, ' ')
        table += "\n"
        table += "Memory size:".ljust(justify_amount, ' ')
        for node in self.nodes_list:
            table += f"{node.memory_size}".rjust(justify_amount, ' ')
        table += "\n"
        table += "Printer no:".ljust(justify_amount, ' ')
        for node in self.nodes_list:
            table += f"{node.printers}".rjust(justify_amount, ' ')
        table += "\n"
        table += "Disk space:".ljust(justify_amount, ' ')
        for node in self.nodes_list:
            table += f"{node.disk_space}".rjust(justify_amount, ' ')
        table += "\n"
        table += "Disk Band:".ljust(justify_amount, ' ')
        for node in self.nodes_list:
            table += f"{node.disk_band}".rjust(justify_amount, ' ')
        table += "\n"
        table += "Printer Band:".ljust(justify_amount, ' ')
        for node in self.nodes_list:
            table += f"{node.printer_band}".rjust(justify_amount, ' ')
        table += "\n"
        print(table)
