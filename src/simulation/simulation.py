from src.graph.graph import Graph
from src.simulation.drone import Drone


class Simulation:
    def __init__(
        self,
        graph: Graph,
        drone: Drone,
        path: list[str],
    ) -> None:
        self.graph = graph
        self.drone = drone
        self.path = path

        self.turn = 0
        self.path_index = 0

    def run(self) -> None:
        print("\n=== SIMULATION START ===")

        while not self.drone.delivered:
            self.turn += 1

            self._execute_turn()

        print("\n=== SIMULATION END ===")

    def _execute_turn(self) -> None:
        if self.path_index >= len(self.path) - 1:
            self.drone.delivered = True
            return

        next_zone = self.path[self.path_index + 1]

        self.drone.current_zone = next_zone

        self.path_index += 1

        print(
            f"Turn {self.turn}: "
            f"D{self.drone.drone_id}-{next_zone}"
        )

        if next_zone == self.graph.end:
            self.drone.delivered = True