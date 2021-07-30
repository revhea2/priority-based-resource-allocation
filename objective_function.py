class ObjectiveFunction:

    def __init__(self, resources):
        self.resources = resources

    def calculate_cost(self, app):
        z = 0

        # for hard disk
        z += app.disk_size / self.resources.get_total_disk()

        for program in app.programs:
            # for main memory
            z += program.number * program.memory_size / self.resources.get_program_total_memory(program)

            # for resident programs
            z += program.number / self.resources.get_program_total_share(program)
        # for printers
        z += app.printers / self.resources.get_total_printers()

        print(f"Application id: {app.app_id} cost: {z}")
        return z

    def objective_function(self, pool):
        print("Currently in Objective Function: ")
        for apps in pool:
            apps.sort(key=lambda x: self.calculate_cost(x))
        print("\n")
        print("Applications inside the pool are sorted:")
        for index, _pool in enumerate(pool):
            print(f"Pool {index}: ", end="")
            for app in _pool:
                print(f"{app};", end=" ")
            print()

        print("--------------------------------- End of Objective Function's job ---------------------------------")
        print()
