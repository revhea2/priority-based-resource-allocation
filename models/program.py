class Program:

    def __init__(self, program_id, program_name, memory_size):
        self.program_name = program_name
        self.program_id = program_id
        self.memory_size = memory_size
        self.number = 1

    def __eq__(self, other):
        return self.program_id == other.program_id

    def __repr__(self):
        return f"Program id: {self.program_id}"
