import heapq

from src.constants import ZoneType
from src.graph.graph import Graph


class Pathfinder:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def shortest_path(
        self,
        start: str,
        end: str,
    ) -> list[str]:
        queue: list[tuple[float, str, list[str]]] = []

        heapq.heappush(
            queue,
            (0.0, start, [start]),
        )

        visited: dict[str, float] = {}

        while queue:
            current_cost, current_node, path = (
                heapq.heappop(queue)
            )

            if current_node == end:
                return path

            if (
                current_node in visited
                and visited[current_node] <= current_cost
            ):
                continue

            visited[current_node] = current_cost

            node = self.graph.nodes[current_node]

            for neighbor_name in node.neighbors:
                neighbor = self.graph.nodes[neighbor_name]

                if neighbor.zone_type == ZoneType.BLOCKED:
                    continue

                move_cost = float(
                    neighbor.movement_cost()
                )

                # Prefer priority zones slightly
                if neighbor.zone_type == ZoneType.PRIORITY:
                    move_cost -= 0.1

                new_cost = current_cost + move_cost

                heapq.heappush(
                    queue,
                    (
                        new_cost,
                        neighbor_name,
                        path + [neighbor_name],
                    ),
                )

        return []

    def path_cost(self, path: list[str]) -> float:
        if len(path) < 2:
            return 0

        total = 0.0

        for node_name in path[1:]:
            node = self.graph.nodes[node_name]

            cost = float(node.movement_cost())

            if node.zone_type == ZoneType.PRIORITY:
                cost -= 0.1

            total += cost

        return total

    def k_shortest_paths(
            self,
            start: str,
            end: str,
            k: int = 3
            ) -> list[list[str]]:
        paths: list[list[str]] = []

        first_path = self.shortest_path(start, end)

        if not first_path:
            return paths

        paths.append(first_path)

        for _ in range(k - 1):
            best_candidate = None
            best_cost = float("inf")

            for existing_path in paths:
                for i in range(len(existing_path) - 1):
                    a = existing_path[i]
                    b = existing_path[i + 1]

                    graph_copy = self.graph.clone()

                    edge_key = tuple(sorted((a, b)))

                    if edge_key not in graph_copy.edges:
                        continue

                    del graph_copy.edges[edge_key]

                    graph_copy.nodes[a].neighbors.pop(b, None)
                    graph_copy.nodes[b].neighbors.pop(a, None)

                    candidate = Pathfinder(
                        graph_copy).shortest_path(start, end)

                    if not candidate:
                        continue

                    cost = self.path_cost(candidate)

                    if cost < best_cost:
                        best_candidate = candidate
                        best_cost = cost

            if (
                best_candidate is None
                or best_candidate in paths
            ):
                break

            paths.append(best_candidate)

        return paths
