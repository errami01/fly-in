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