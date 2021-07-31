class Node:

    def __init__(self, node_id, disk_space, memory_size, printers, resident_program, program_shareability, disk_band,
                 printer_band):
        self.node_id = node_id
        self.resident_program = resident_program
        self.program_shareability = program_shareability
        self.memory_size = memory_size
        self.printers = printers
        self.disk_space = disk_space
        self.neighbors = {}
        self.disk_band = disk_band
        self.printer_band = printer_band

    def __repr__(self):
        output = f"""
        Node id: {self.node_id}
        Programs: {self.resident_program}
        Share: {self.program_shareability}
        Memory Size: {self.memory_size}
        Printers: {self.printers}
        Disk Space: {self.disk_space}
        """

        return output
