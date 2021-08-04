class VDA:

    def __init__(self, graph):
        self.graph = [
            [0, 0, 13, 0, 16, 8],
            [0, 0, 0, 6, 0, 10],
            [13, 0, 0, 16, 0, 11],
            [0, 6, 16, 0, 5, 17],
            [16, 0, 0, 5, 0, 7],
            [8, 10, 11, 17, 7, 0],
        ]
        self.band = None
        self.pre = None

    @staticmethod
    def get_maximum_band(band, s):
        max_index = -1
        max_value = -1
        for index, value in enumerate(band):
            if index in s and max_value < value:
                max_value = value
                max_index = index

        return max_index

    def variant_dijkstra_algorithm(self, start, v):
        i = start
        s = {1, 2, 3, 4, 5}
        current = start

        band = [0, 0, 0, 0, 0, 0]
        pre = [0, 0, 0, 0, 0, 0]

        while i < v:

            for vj in s:
                if self.graph[current][vj] > 0:
                    if band[vj] == 0:
                        band[vj] = self.graph[current][vj]
                        pre[vj] = current
                    elif band[vj] < min(band[current], self.graph[current][vj]):
                        band[vj] = min(band[current], self.graph[current][vj])
                        pre[vj] = current
            u = self.get_maximum_band(band, s)
            if u != -1:
                s.remove(u)
                current = u

            i += 1

        # set global vlaues
        self.band = band
        self.pre = pre

        # print("PRE List")
        # print(pre)
        # print("<--------------->")

        paths = [[] for _ in range(v)]
        for j in range(1, v):
            paths[j].append(j)
            u = j
            while pre[u] != 0:
                paths[j].append(pre[u])
                u = pre[u]

            paths[j].append(0)
            paths[j] = paths[j][::-1]

        return paths

    def check_bandwidth(self, node_id):
        return self.band[node_id]

    def allocate_band(self, node_id, band_allocated):
        self.band[node_id] -= band_allocated
        self.graph[node_id][self.pre[node_id]] -= band_allocated
        self.graph[self.pre[node_id]][node_id] -= band_allocated

    def re_allocate_band(self, node_id, pre, band_allocated):
        self.band[node_id] += band_allocated
        self.graph[node_id][pre] += band_allocated
        self.graph[pre][node_id] += band_allocated

    def view_graph(self):
        print("Graph Adjacency Matrix:")
        for arr in self.graph:
            print(arr)
        print()


if __name__ == '__main__':
    VDA(None).variant_dijkstra_algorithm(0, 6)
