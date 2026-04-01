from typing import Any


class EdmondsKarp:
    def __init__(self, C: list[list[int]], s: int, e: int,
                 priority: set[Any] | None = None) -> None:
        """Initialize Edmonds-Karp with a capacity matrix, source, sink, and
           optional priority nodes"""
        self.C = C
        self.s = s
        self.e = e
        self.priority: set[Any] = priority or set()

    def create_matrice_F(self) -> tuple[list[list[int]], int]:
        """Run Edmonds-Karp and return the flow matrix with the total flow
           value"""
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
        """Find an augmenting path from s to e via BFS, prioritizing priority
           nodes"""
        queue = [s]
        paths: dict[int, list[tuple[int, int]]] = {s: []}
        if s == e:
            return paths[s]
        while queue:
            u = queue.pop(0)
            neighbors = sorted(range(len(C)),
                               key=lambda v: v not in self.priority)
            for v in neighbors:
                if (C[u][v] - F[u][v] > 0) and v not in paths:
                    paths[v] = paths[u] + [(u, v)]
                    if v == e:
                        return paths[v]
                    queue.append(v)
        return None
