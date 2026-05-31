from src.graph.pathfinder import Pathfinder


class RouteAllocator:
    def __init__(self, graph):
        self.graph = graph
        self.pathfinder = Pathfinder(graph)

    def allocate(
            self,
            drone_count: int
            ) -> dict[int, list[str]]:
        paths = self.pathfinder.k_shortest_paths(
            self.graph.start,
            self.graph.end,
            k=3
            )

        if not paths:
            raise ValueError(
                "No valid path found"
            )

        assignments = {}

        for drone_id in range(
            1,
            drone_count + 1,
        ):
            assignments[drone_id] = paths[
                (drone_id - 1)
                % len(paths)
            ]

        return assignments

    