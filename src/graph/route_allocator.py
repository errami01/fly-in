from src.graph.pathfinder import Pathfinder
from src.graph.route_assignment import RouteAssignment


class RouteAllocator:
    def __init__(self, graph) -> None:
        self.graph = graph
        self.pathfinder = Pathfinder(graph)

    def allocate(self, drone_count: int) -> dict[int, list[str]]:
        paths = self.pathfinder.k_shortest_paths(
            self.graph.start,
            self.graph.end,
            k=3
            )

        if not paths:
            raise ValueError("No valid path found")

        assignments: dict[int, list[str]] = {}

        for drone_id in range(1, drone_count + 1):
            routes = [RouteAssignment(path)for path in paths]

        for drone_id in range(1, drone_count + 1):
            best_route = min(routes, key=self._route_score)
            assignments[drone_id] = (best_route.path)
            best_route.assigned_drones += 1
        print("\n=== ROUTE ASSIGNMENTS ===")

        for drone_id, path in assignments.items():
            print(
                f"D{drone_id}: "
                + " -> ".join(path)
            )
        return assignments

    def _route_score(self, route: RouteAssignment) -> float:
        path_cost = self.pathfinder.path_cost(route.path)
        congestion_penalty = (route.assigned_drones * 2.0)
        capacity_penalty = self._capacity_penalty(route.path)
        return path_cost + congestion_penalty + capacity_penalty

    def _capacity_penalty(self, path: list[str]) -> float:
        penalty = 0.0

        for node_name in path:
            node = self.graph.nodes[node_name]

            if node.max_drones <= 1:
                penalty += 1.0

        return penalty


# class RouteAllocator:
#     def __init__(self, graph):
#         self.graph = graph
#         self.pathfinder = Pathfinder(graph)

#     def allocate(self, drone_count: int) -> dict[int, list[str]]:
#         paths = self.pathfinder.k_shortest_paths(
#             self.graph.start,
#             self.graph.end,
#             k=3
#             )

#         if not paths:
#             raise ValueError("No valid path found")

#         assignments: dict[int, list[str]] = {}

#         for drone_id in range(1, drone_count + 1):
#             routes = [RouteAssignment(path)for path in paths]

#         for drone_id in range(1,drone_count + 1):
#             best_route = min(routes, key=self._route_score)
#             assignments[drone_id] = (best_route.path)
#             best_route.assigned_drones += 1
#         print("\n=== ROUTE ASSIGNMENTS ===")

#         for drone_id, path in assignments.items():
#             print(
#                 f"D{drone_id}: "
#                 + " -> ".join(path)
#             )
#         return assignments


#     def _route_score(
#     self,
#     route: RouteAssignment,
# ) -> float:
#         path_cost = self.pathfinder.path_cost(
#             route.path
#         )

#         bottleneck = self._path_bottleneck(
#             route.path
#         )

#         score = path_cost

#         # Penalize only when the route is
#         # already predicted to be full
#         if route.assigned_drones >= bottleneck:
#             score += 1000

#         return score

#     def _path_bottleneck(
#     self,
#     path: list[str],
# ) -> int:
#         bottleneck = float("inf")

#         for node_name in path:
#             node = self.graph.nodes[node_name]

#             if (
#                 node_name in (
#                     self.graph.start,
#                     self.graph.end,
#                 )
#             ):
#                 continue

#             bottleneck = min(
#                 bottleneck,
#                 node.max_drones,
#             )

#         return (
#             int(bottleneck)
#             if bottleneck != float("inf")
#             else 1
#         )
