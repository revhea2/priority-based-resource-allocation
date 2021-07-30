class Dispatcher:

    def __init__(self):
        self.a = 0

    def get_total_program(self, apps, program, nodes):
        prg = 0
        node_prg = 0
        for app in apps:
            p = app.get_program(program)
            if p:
                prg += p.number

        for node in nodes:
            if node.resident_program and node.resident_program == program:
                node_prg += node.program_shareability

        return [prg, node_prg]

    def get_total_printer(self, apps, nodes):
        app_printer = 0
        nodes_printer = 0

        for app in apps:
            app_printer += app.printers
        for node in nodes:
            nodes_printer += node.printers

        return [app_printer, nodes_printer]

    def get_total_disk(self, apps, nodes):
        total_app_disk_size = 0
        total_node_disk_space = 0

        for app in apps:
            total_app_disk_size += app.disk_size

        for node in nodes:
            total_node_disk_space += node.disk_space

        return [total_app_disk_size, total_node_disk_space]

    def pool_dispatch(self, pool, priority, apps):

        dispatched = []

        for i in range(len(priority)):
            # todo: use index and remove the app in apps after the conditions

            if type(priority[i][0]) == str and priority[i][0] == "printer":
                for app in apps:
                    if app.app_id not in dispatched:
                        if app.printers > 0:
                            pool[i].append(app)
                            dispatched.append(app.app_id)
            elif type(priority[i][0]) == str and priority[i][0] == "harddisk":
                for app in apps:
                    if app.app_id not in dispatched:
                        if app.disk_size > 0:
                            pool[i].append(app)
                            dispatched.append(app.app_id)
            else:
                for app in apps:
                    if app.app_id not in dispatched:
                        if app.get_program(priority[i][0]):
                            pool[i].append(app)
                            dispatched.append(app.app_id)

    def dispatch(self, apps, programs, m, nodes):
        priority = [0] * m

        apps_total_disk, nodes_total_disk = self.get_total_disk(apps, nodes)
        priority[0] = ["harddisk", apps_total_disk / nodes_total_disk]

        for i in range(1, m - 1):
            apps_total_prg, nodes_total_prg = self.get_total_program(apps, programs[i - 1], nodes)
            priority[i] = [programs[i - 1], apps_total_prg / nodes_total_prg]

        app_printers, nodes_printers = self.get_total_printer(apps, nodes)
        priority[m - 1] = ["printer", app_printers / nodes_printers]

        print("Dispatcher priority: ")
        for prio in priority:
            print(prio)

        print()

        # sorts the priority
        priority.sort(key=lambda x: -x[1])

        print("Sorted Dispatcher priority: ")
        for prio in priority:
            print(prio)

        print()

        pool = [[] for _ in range(m)]

        self.pool_dispatch(pool, priority, apps)

        return pool
