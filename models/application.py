class Application:

    def __init__(self, app_id, app_name, disk_size, programs, printers):
        self.app_id = app_id
        self.app_name = app_name
        self.disk_size = disk_size
        self.programs = programs
        self.printers = printers

    def get_program(self, other):
        for program in self.programs:
            if program == other:
                return program
        return None

    def __repr__(self):
        return f"Application id: {self.app_id}"

    def __str__(self):
        return f"Application id: {self.app_id}"
