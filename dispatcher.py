class Dispatcher:

    def __init__(self):
        self.a = 0

    @staticmethod
    def get_app_total_disk(apps):
        total_app_disk_size = 0
        for app in apps:
            total_app_disk_size += app.disk_size
        return total_app_disk_size

    @staticmethod
    def get_app_total_printers(apps):
        total_app_printers = 0
        for app in apps:
            total_app_printers += app.printers
        return total_app_printers

    @staticmethod
    def get_app_total_programs(apps, program):
        total_app_programs = 0
        for app in apps:
            p = app.get_program(program)
            if p:
                total_app_programs += p.number
        return total_app_programs

    @staticmethod
    def pool_dispatching(pool, resource_priority, apps):
        # we need this to efficiently allocate an app to the pool
        apps_mapped = {}
        for app in apps:
            apps_mapped[app.app_id] = app

        for index, priority in enumerate(resource_priority):
            resource_type = priority[0]

            # if all apps are added in the pool
            if not apps_mapped:
                return pool
            keys = []

            if type(resource_type) == str and resource_type == "printer":
                for key, value in apps_mapped.items():
                    if value.printers > 0:
                        pool[index].append(value)
                        keys.append(key)
            elif type(resource_type) == str and resource_type == "hard_disk":
                for key, value in apps_mapped.items():
                    if value.disk_size > 0:
                        pool[index].append(value)
                        keys.append(key)
            else:
                for key, value in apps_mapped.items():
                    if value.get_program(resource_type):
                        pool[index].append(value)
                        keys.append(key)

            for key in keys:
                del apps_mapped[key]

    @staticmethod
    def sort_resource_type_priority(resource_type_priority):
        # print("Currently in Dispatcher:")
        # print("Resource Type Priority: (Unsorted)")
        # for resource_type in resource_type_priority:
        #     print(resource_type)

        resource_type_priority.sort(key=lambda res_type: -res_type[1])

        # print()
        # print("Resource Type Priority: (Sorted) ")
        # for resource_type in resource_type_priority:
        #     print(resource_type)

    def dispatch(self, apps, programs, m, resources):
        resource_type_priority = [0] * m
        pool = [[] for _ in range(m)]
        resource_type_priority[0] = ["hard_disk", self.get_app_total_disk(apps) / resources.get_total_disk()]

        for i in range(1, m - 1):
            resource_type_priority[i] = [programs[i - 1],
                                         self.get_app_total_programs(apps, programs[
                                             i - 1]) / resources.get_program_total_share(programs[i - 1])]

        resource_type_priority[m - 1] = ["printer", self.get_app_total_printers(apps) / resources.get_total_printers()]

        self.sort_resource_type_priority(resource_type_priority)
        self.pool_dispatching(pool, resource_type_priority, apps)

        # print("\n- - - - - - - - - - - - - - - - - -\nThe applications are now dispatched! \n")
        # print("Pool with priority:")
        # for index, _pool in enumerate(pool):
        #     print(f"Pool {index}: ", end="")
        #     for app in _pool:
        #         print(f"{app};", end=" ")
        #     print()
        #
        # print("------------------------------------- End of Dispatcher's job ---------------------------------------")
        # print()

        return pool
