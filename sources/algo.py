class EdmondsKarp:
    def __init__(self, C: list[list[int]], s: int, e: int) -> None:
        self.C = C
        self.s = s
        self.e = e

    def create_matrice_F(self) -> tuple[list[list[int]], int]:
        self.n = len(self.C)
        self.F = [[0] * self.n for i in range(self.n)]
        path = self.bfs(self.C, self.F, self.s, self.e)

        while path is not None:
            flow = min(self.C[u][v] - self.F[u][v] for u, v in path)
            for u, v in path:
                self.F[u][v] += flow
                self.F[v][u] -= flow
            path = self.bfs(self.C, self.F, self.s, self.e)
        return self.F, sum(self.F[self.s][i] for i in range(self.n))

    def bfs(self, C: list[list[int]], F: list[list[int]], s: int,
            e: int) -> list[tuple[int, int]] | None:
        queue = [s]
        paths: dict[int, list[tuple[int, int]]] = {s: []}
        if s == e:
            return paths[s]
        while queue:
            u = queue.pop(0)
            for v in range(self.n):
                if (C[u][v] - F[u][v] > 0) and v not in paths:
                    paths[v] = paths[u] + [(u, v)]
                    if v == e:
                        return paths[v]
                    queue.append(v)
        return None
